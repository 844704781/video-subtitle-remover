from flask import Flask, request, jsonify
import threading
import time
from backend.main import SubtitleRemover

app = Flask(__name__)
tasks = {}


def run_subtitle_remover(task_id, video_path, sub_area):
    def progress_handler(progress):
        tasks[task_id]['progress'] = progress

    sd = SubtitleRemover(video_path, sub_area=sub_area, progress_callback=progress_handler)
    sd.run()
    tasks[task_id]['status'] = 'finished'
    tasks[task_id]['output_file'] = sd.video_out_name


@app.route('/remove_subtitle', methods=['POST'])
def remove_subtitle():
    data = request.json
    task_id = data.get('task_id')
    video_path = data.get('video_path')
    sub_area = data.get('sub_area')

    if not task_id or not video_path:
        return jsonify({'error': 'task_id and video_path are required'}), 400

    if task_id in tasks:
        task = tasks.get(task_id)
        return jsonify({'task_id': task_id, 'progress': task['progress'], 'status': task['status'],
                        'output_file': task.get('output_file')}), 200
    tasks[task_id] = {'progress': 0, 'status': 'running'}
    thread = threading.Thread(target=run_subtitle_remover, args=(task_id, video_path, sub_area))
    thread.start()

    return jsonify({'task_id': task_id, 'status': 'started'}), 200


@app.route('/task_progress/<task_id>', methods=['GET'])
def task_progress(task_id):
    task = tasks.get(task_id)
    if task is None:
        return jsonify({'error': 'Task not found'}), 404

    return jsonify({'task_id': task_id, 'progress': task['progress'], 'status': task['status'],
                    'output_file': task.get('output_file')}), 200


if __name__ == '__main__':
    app.run(debug=False, port=5000, host='127.0.0.1')
