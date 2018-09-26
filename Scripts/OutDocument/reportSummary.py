import Constants
import Dependencies.pdfkit as pdfkit
import os
def returnioscode(keys):
    htmlcode = """

        <!DOCTYPE html>
    <html>
    <head>
    <style>
    
    table {{
    border-collapse: collapse;
    width: 100%;
}}

th, td {{
    text-align: left;
    padding: 8px;
}}

tr:nth-child(even){{background-color: #f2f2f2}}

th {{
    background-color: #236CB6;
    color: white;
}}
    </style>
    </head>
    <body>

    <h2>Report Summary</h2>

    <table style="border-collapse: collapse; width: 100%;">
      <tr>
        <th>#</th>
        <th>Vulnerability Name</th>
        <th>Status</th>
      </tr>
      <tr>
        <td>1</td>
        <td>Insecure App Transport Security</td>
        <td>{}</td>
      </tr>
      <tr>
      <td>2</td>
        <td>Scan For Declared URL Schemes</td>

        <td>{}</td>
      </tr>
      <tr>
        <td>3</td>
        <td>CryptID Scan</td>
        <td>{}</td>
      </tr>
      <tr>
        <td>4</td>
        <td>Stack Smash Protection Scan</td>
        <td>{}</td>
      </tr>
      <tr>
        <td>5</td>
        <td>Pie Flag Vulnerability Scan</td>
        <td>{}</td>
      </tr>
      <tr>
        <td>6</td>
        <td>Automatic Reference Counting</td>
        <td>{}</td>
      </tr>
      <tr>
        <td>7</td>
        <td>Third Party Frameworks Scan</td>
        <td>{}</td>
      </tr>

    </table>

    </body>
    </html>

        """.format(keys[0],keys[1],keys[2],keys[3],keys[4],keys[5],keys[6])
    return htmlcode

def returnandroidcode(keys):
    htmlcode = """

            <!DOCTYPE html>
        <html>
        <head>
        <style>

        table {{
        border-collapse: collapse;
        width: 100%;
    }}

    th, td {{
        text-align: left;
        padding: 8px;
    }}

    tr:nth-child(even){{background-color: #f2f2f2}}

    th {{
        background-color: #236CB6;
        color: white;
    }}
        </style>
        </head>
        <body>

        <h2>Report Summary</h2>

        <table style="border-collapse: collapse; width: 100%;">
          <tr>
            <th>#</th>
            <th>Vulnerability Name</th>
            <th>Status</th>
          </tr>
          <tr>
            <td>1</td>
            <td>Signing Info Verification</td>
            <td>{}</td>
          </tr>
          <tr>
          <td>2</td>
            <td>Android XML Content Verification</td>

            <td>{}</td>
          </tr>
          <tr>
            <td>3</td>
            <td>Permissions Scan</td>
            <td>{}</td>
          </tr>
          <tr>
            <td>4</td>
            <td>Smali Files Scan</td>
            <td>{}</td>
          </tr>
          <tr>
            <td>5</td>
            <td>Asset Folder Scan</td>
            <td>{}</td>
          </tr>

        </table>

        </body>
        </html>

            """.format(keys[0], keys[1], keys[2], keys[3], keys[4])
    return htmlcode

def returnpdfcode(config,platform):
    status = []

    for keys, values in config.items():
        status.append(config[keys][Constants.STATUS])
    if platform == "Android":
        string = returnandroidcode(status)
    else:
        string = returnioscode(status)


    file_name = "OutDocument/temp.htm"
    with open(file_name, 'w') as file:
        file.write(string)
    pdffilename = "pdf_related_files/reportSummary.pdf"
    pdfkit.from_file("OutDocument/temp.htm",pdffilename)



