from flask import Flask, request, render_template, jsonify
from joblib import load
from waitress import serve
import pandas as pd
import warnings; warnings.simplefilter('ignore')

model = load('./model.joblib')

app = Flask(__name__)

feature_columns = [
  'locus_abc',
  'locus_dr',
  'locus_dq',
  'locus_dp',
  'panel_nc',
  'panel_pc',
  'panel_allele_count',
  'panel_min_mfi',
  'panel_max_mfi',
]

@app.route('/', methods=['GET'])
def index():
  return render_template('index.html')

@app.route('/version', methods=['GET'])
def version():
  return '2026-05-09'

@app.route('/predict', methods=['GET', 'POST'])
def predict():
  try:
    eplet_locus = request.args.get('eplet_locus', '').lower()

    eplet_data = pd.DataFrame([[(0, 1)[eplet_locus == 'abc'],
                                (0, 1)[eplet_locus == 'drb'],
                                (0, 1)[eplet_locus == 'dq'],
                                (0, 1)[eplet_locus == 'dp'],
                                int(request.args.get('panel_nc')),
                                int(request.args.get('panel_pc')),
                                int(request.args.get('eplet_allele_count')),
                                int(request.args.get('eplet_min_mfi')),
                                int(request.args.get('eplet_max_mfi'))]],
                              columns=feature_columns)

    results = model.predict(eplet_data)
    probabilities = model.predict_proba(eplet_data)

    return jsonify(
      label=str(results[0]),
      score0=str(probabilities[0][0]),
      score1=str(probabilities[0][1]),
    )
  except:
    return 'Check if all params (eplet_locus, eplet_allele_count, eplet_min_mfi, eplet_max_mfi, panel_nc, panel_pc) contain valid values.', 500

if __name__ == '__main__':
  # app.run(host='0.0.0.0', port=5000, threaded=True)
  serve(app, host='0.0.0.0', port=80, threads=2)
