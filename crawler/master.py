from flask import request
import transport
import random
import logic
# the master is also a slave (that can handle job requests)
slaves = set([("127.0.0.1", transport.PORT)])
results = []
processing_status = []


def decorate(webapp):
    @webapp.route("/", methods=['POST'])
    def start():
        global results
        global processing_status
        requests = request.get_data(as_text=True).split('\n')
        job_id = len(results)
        results.append(logic.identity_result())
        processing_status.append({})
        for r in requests:
            s = random.choice(list(slaves))
            request_json = {}
            request_json["jobid"] = job_id
            request_json["content"] = r
            info = logic.marshall_info(logic.init_info())
            request_json["info"] = info
            processing_status[job_id][(r, info)] = "processing"
            transport.send_work(s[0], s[1], request_json)
        return str(job_id)

    @webapp.route("/result/<int:index>", methods=['GET'])
    def result(index):
        return logic.marshall_result(results[index])

    @webapp.route("/status/<int:index>", methods=['GET'])
    def status(index):
        status = ""
        global processing_status
        for r, info in processing_status[index]:
            if logic.status_filter(r, info):
                status += "%s -- %s\n" % (r, processing_status[index][r, info])
        return status

    @webapp.route("/join", methods=['POST'])
    def join():
        print request.remote_addr
        slaves.add(request.remote_addr, transport.PORT)
        return "ok"

    @webapp.route("/presult", methods=['POST'])
    def presult():
        global processing_status
        global results
        j = request.get_json()
        for r in j["requests"]:
            s = random.choice(list(slaves))
            request_json = {}
            request_json["jobid"] = j["jobid"]
            request_json["content"] = r["content"]
            request_json["info"] = r["info"]
            transport.send_work(s[0], s[1], request_json)
        k = (j["origin_request"], logic.unmarshall_info(j["origin_info"]))
        processing_status[j["jobid"]][k] = "done"
        results[j["jobid"]] = logic.combine(results[j["jobid"]],
                                            logic.unmarshall_result(j["result"]))
        return "ok"
