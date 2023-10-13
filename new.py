from flask import Flask, request, jsonify
import requests
import datetime
import json


app = Flask(__name__)

YOUTUBE_API_URL = 'https://app.ylytic.com/ylytic/test'


with open('data.json', 'r') as file:
    sample_data = json.load(file)

@app.route('/search', methods=['GET'])
def search_comments():
    search_author = request.args.get('search_author')
    at_from = request.args.get('at_from')
    at_to = request.args.get('at_to')
    like_from = int(request.args.get('like_from'))
    like_to = int(request.args.get('like_to'))
    reply_from = request.args.get('reply_from')
    reply_to = request.args.get('reply_to')
    search_text = request.args.get('search_text')

    filtered_comments = []

    for comment in sample_data['comments']:
        comment_date = datetime.datetime.strptime(comment['at'], '%a, %d %b %Y %H:%M:%S %Z')

        # Apply filters
        if (not search_author or search_author.lower() in comment['author'].lower()) and \
           (not at_from or datetime.datetime.strptime(at_from, '%d-%m-%Y') <= comment_date <= datetime.datetime.strptime(at_to, '%d-%m-%Y')) and \
           (not like_from or like_from <= comment['like'] <= like_to) and \
           (not reply_from or reply_from <= comment['reply'] <= reply_to) and \
           (not search_text or search_text.lower() in comment['text'].lower()):
            filtered_comments.append(comment)

    return jsonify({'comments': filtered_comments})

if __name__ == '__main__':
    app.run(debug=True)
