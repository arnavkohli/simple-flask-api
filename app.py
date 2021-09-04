import os, csv, sys
import pandas as pd
from dotenv import load_dotenv
from flask import Flask, jsonify, request

if not sys.version.startswith("3.7"):
	exit("Please upgrade your python version to 3.7.x (current: {}".format(sys.version.split(" ")[0]))


# Set env Variables
load_dotenv()
CSV_FILE_PATH = os.getenv("CSV_FILE_PATH")
PORT = os.getenv("PORT")


# Copying state of db at the time of server boot up.
# This is done to eradicate redundant opening of the db file.
try:
	# Copy state of db and store it so that we dont have to open the file redundantly 
	db = pd.read_csv(CSV_FILE_PATH).to_dict("records")
except Exception as err:
	raise Exception(f"[ERROR] There was an error in loading the CSV file: {err}")

app = Flask(__name__)

def get_distance_in_kms(startStationData, endStationData):
	return abs(startStationData.get("Distance in Kms") - endStationData.get("Distance in Kms"))


@app.route("/getAll", methods=['GET'])
def get_all():
	try:
		return jsonify(db), 200
	except Exception as err:
		return jsonify({"msg": err}), 500

@app.route("/search", methods=['GET'])
def search():
	if not request.args.get("station") or request.args.get("station").strip() == "":
		return jsonify({"msg": "`station` parameter not found in request."}), 400

	query = request.args.get("station")
	results = []
	result_count = 0
	for record in db:
		if query in record.get("Station"):
			results.append(record)
			result_count += 1

	return jsonify({"result_count" : result_count, "results" : results}), 200


@app.route("/distance", methods=['GET'])
def distance():
	if not request.args.get("startStation") and not request.args.get("endStation"):
		return jsonify({"msg": "`startStation` and `endStation` parameters not found in request."})
	if not request.args.get("startStation"):
		return jsonify({"msg": "`startStation` parameter not found in request."})
	if not request.args.get("endStation"):
		return jsonify({"msg": "`endStation` parameter not found in request."})
	if request.args.get("startStation") == request.args.get("endStation"):
		return jsonify({"msg" : "`startStation` and `endStation` cannot be the same."})

	startStationCode = request.args.get("startStation").upper()
	endStationCode   = request.args.get("endStation").upper()

	startStationData, endStationData = None, None

	for record in db:

		if record.get("Station Code") == startStationCode:
			if endStationData:
				# check if stations are on the same line
				if endStationData.get("Connection") == record.get("Connection"):
					# calculate and return distance
					return jsonify({"distance_in_kms": get_distance_in_kms(startStationData=record, endStationData=endStationData)}), 200
				else:
					return jsonify({"msg": f"`startStation` and `endStation` should be on the same line/ connection."}), 400
			else:
				startStationData = record

		elif record.get("Station Code") == endStationCode:
			if startStationData:
				# check if stations are on the same line
				if startStationData.get("Connection") == record.get("Connection"):
					# calculate and return distance
					return jsonify({"distance_in_kms": get_distance_in_kms(startStationData=startStationData, endStationData=record)}), 200
				else:
					return jsonify({"msg": f"`startStation` and `endStation` should be on the same line/ connection."}), 400
			else:
				endStationData = record

	if not startStationData and not endStationData:
		return jsonify({"msg" : "`startStation` and `endStation` codes are invalid."}), 400
	if not startStationData:
		return jsonify({"msg" : "`startStation` code is invalid."}), 400
	if not endStationData:
		return jsonify({"msg" : "`endStationData` code is invalid."}), 400

if __name__ == "__main__":
	app.run(port=PORT)



