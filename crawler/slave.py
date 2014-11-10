from flask import request
import threading
import logic
import transport


def do_work(addr, job_id, request, info):
    result, new_request = logic.do_work(request, info)
    to_send = {}
    to_send["result"] = logic.marshall_result(result)
    to_send["origin_request"] = request
    to_send["origin_info"] = info
    to_send["jobid"] = job_id
    to_send["requests"] = [{"content": content, "info": info} for content,
                           info in new_request]
    transport.send_result(addr, transport.PORT, to_send)


def decorate(webapp, master_port):
    @webapp.route("/work", methods=['POST'])
    def work():
        j = request.get_json()
        info = logic.unmarshall_info(j["info"])
        remote_addr = request.remote_addr
        job_id = j["jobid"]
        t = threading.Thread(target=do_work, args=(remote_addr, job_id,
                                                   j["content"],
                                                   info))
        t.start()
        return "ok"
