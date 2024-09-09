from datetime import datetime
import requests
from flask import Flask, jsonify

app = Flask(__name__)

SOURCE_API_URL = 'http://localhost:8080/v1/categories?page=1&limit=50&sort=title&sortDesc=false'


@app.route('/api/categories/sync', methods=['GET'])
def sync_category_data():
    try:
        # Fetch data from source API and transform it into a suitable format
        res = requests.get(SOURCE_API_URL)
        # Check response
        if res.status_code != 200:
            return jsonify({"statusCode": 500, "message": "Error fetching data from source API"}), 500

        # Extract and transform data as needed
        categories = res.json()['data']

        if not categories:
            return jsonify({"statusCode": 200, "message": "No categories found"}), 200

        cat = []
        for c in categories:
            days = get_diff_date(c['startDate'])

            cat.append({
                'id': c['catalogId'],
                'title': c['title'],
                'days': '{d} days'.format(d = days),
            })

        return jsonify({"statusCode": 200, "message": "Success", "data": cat})
    except TypeError:
        return jsonify({"statusCode": 500, "message": "Internal Server Error"})


def get_diff_date(date):
    try:
        start_date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        now = datetime.now()
        diff = abs((now - start_date).days)

        return diff
    except ValueError:
        return None


if __name__ == '__main__':
    app.run()
