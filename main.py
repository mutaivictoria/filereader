from flask import Flask, render_template, request, redirect, url_for,send_file
import pandas as pd
import os
import helperfunctions.readerfunctions as helper


app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/',methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if the post request has the file part
       
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        print(file.filename)

        # If user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return redirect(request.url)

        if file:
            # Save the uploaded PDF file
            pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], 'input.pdf')
            file.save(pdf_path)

            # Specify the CSV file name
            csv_name = 'output.xlsx'

            # Process the PDF file and write to CSV
            df = helper.read_table(pdf_path)

            df.to_excel(csv_name, index=False, header=False,engine='openpyxl')
            return render_template('index.html', filename=csv_name)
    return render_template("index.html")

@app.route('/phoenix',methods=['GET', 'POST'])
def phoenix():
    if request.method == 'POST':
        # Check if the post request has the file part
       
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        print(file.filename)

        # If user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return redirect(request.url)

        if file:
            # Save the uploaded PDF file
            pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], 'input.pdf')
            file.save(pdf_path)

            # Specify the CSV file name
            csv_name = 'output.xlsx'

            # Process the PDF file and write to CSV
            df = helper.read_phoenix_table(pdf_path)

            df.to_excel(csv_name, index=False, header=False,engine='openpyxl')
            return render_template('phoenix.html', filename=csv_name)
    return render_template("phoenix.html")

@app.route('/download/<filename>')
def download_file(filename):
    csv_path = os.path.join(filename)
    return send_file(csv_path, as_attachment=True)

if __name__ == "__main__":
    app.run(host='0.0.0.0')