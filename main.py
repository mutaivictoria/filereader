from flask import Flask, render_template, request, redirect, url_for,send_file
import pandas as pd
import os
import helperfunctions.readerfunctions as helper


app = Flask(__name__)

UPLOAD_FOLDER = '/tmp'
ALLOWED_EXTENSIONS = {'pdf'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/',methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if the post request has the file part
       
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']

        # If user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return redirect(request.url)

        if file:
            # Save the uploaded PDF file
            pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(pdf_path)
            # Specify the Excel file name with the /tmp directory path
            excel_name = os.path.join(app.config['UPLOAD_FOLDER'], os.path.splitext(file.filename)[0] + '.xlsx')

            # Process the PDF file and write to Excel
            df = helper.read_table(pdf_path)

            # Save the Excel file to the /tmp directory
            df.to_excel(excel_name, index=False, header=False, engine='openpyxl')

            return render_template('index.html', filename=excel_name)
    return render_template("index.html")

@app.route('/phoenix',methods=['GET', 'POST'])
def phoenix():
    if request.method == 'POST':
        # Check if the post request has the file part
       
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']

        # If user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return redirect(request.url)

        if file:
            # Save the uploaded PDF file
            pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(pdf_path)

            # Specify the CSV file name
            csv_name = os.path.splitext(file.filename)[0] +'.xlsx'

            # Process the PDF file and write to CSV
            df = helper.read_phoenix_table(pdf_path)

            df.to_excel(csv_name, index=False, header=False,engine='openpyxl')
            return render_template('phoenix.html', filename=csv_name)
    return render_template("phoenix.html")

@app.route('/verify')
def verify_files():
    return render_template("verification.html")

@app.route('/scanned_pdfs')
def scanned_files():
    return render_template("scanned.html")

@app.route('/rename_files')
def rename_files():
    return render_template("rename.html")

@app.route('/download/<filename>')
def download_file(filename):
    csv_path = os.path.join(filename)
    return send_file(csv_path, as_attachment=True)

if __name__ == "__main__":
    app.run(host='0.0.0.0')