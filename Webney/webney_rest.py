import json, sys, os
from flask import Flask, request, jsonify
import logging
from threading import Thread
logs = []

try:
    from sims4communitylib.utils.common_time_utils import CommonTimeUtils
    logs.append("* S4CL Imported!")
except Exception as e:
    logs.append("* S4CL import error. {}".format(e))

try: import webney_command_handler
except: logs.append("* Command handler --> FALSE")

try:
    from sims4.commands import Command, CommandType, CheatOutput
    logs.append("* Sims Hook --> TRUE")
    hookedToSims = True
except:
    logs.append("* Sims Hook --> FALSE")
    hookedToSims = False

def run_rest():
    logs.append("* Webney REST_API ONLINE!")
    try:
        sys.stdout.isatty = lambda: False
        sys.stderr.isatty = lambda: False
        app = Flask(__name__)
        log = logging.getLogger('werkzeug')
        logging.getLogger('werkzeug').disabled = True
        os.environ['WERKZEUG_RUN_MAIN'] = 'true'

        @app.route('/updates', methods=['GET'])
        def get_updates():
            log_output = ""
            for x in logs:
                log_output += x + "\n"
            return jsonify({
                'logs': log_output,
            })

        @app.route('/datetime', methods=['GET'])
        def getdatetime():
            s4dt = CommonTimeUtils.get_current_date_and_time()
            hour = CommonTimeUtils.get_current_hour(s4dt)
            minute = CommonTimeUtils.get_current_minute(s4dt)
            second = CommonTimeUtils.get_current_second(s4dt)
            if CommonTimeUtils.is_day_time():
                ampm = "AM"
            else:
                ampm = "PM"
            
            if CommonTimeUtils.game_is_paused(): paused = True
            else: paused = False

            return jsonify({
                'hour': hour,
                'minute': minute,
                'second': second,
                'ampm': ampm,
                'paused': paused,
            })

        @app.route('/status', methods=['GET'])
        def query_records():
            return jsonify({
                'modversion': '0.1',
                'author': 'MatroSka',
                'sims_hook': hookedToSims
            })

        @app.route('/command/<command>', methods=['GET'])
        def issueCommand(command):
            output = ""
            try:
                output = webney_command_handler.process_command(command)
                output_type = "success"
                logs.append("* Successfully ran command {}".format(command))
            except Exception as e: 
                output = "{}".format(e)
                output_type = "error"
                logs.append("* Error running command {}".format(command))
            return jsonify({
                "issued_command": command,
                "output": output,
                "output_type": output_type
            })
        app.run(host='0.0.0.0', debug=False, port=2132)
    except Exception as e:
        return str(e)

rest_thread = Thread(target=run_rest)
#rest_thread.setDaemon(True)
rest_thread.start()