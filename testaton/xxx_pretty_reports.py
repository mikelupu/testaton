import time
import markdown
from pandas import DataFrame, options

def generate_test_html(testSql, results):
    """Accepts a pandas dataframe and turns it into a table"""
    test_description = '''<table border="0">
                        <tr><td><b>Name: </b></td><td>''' + testSql.name + '''</td></tr>
                        <tr><td><b>Filename: </b></td><td>''' + testSql.file_name + '''</td></tr>
                        <tr><td><b>Description: </b></td><td>''' + testSql.description + '''</td></tr>
                        <tr><td><b>Variables:</b></td><td>''' + str(testSql.substitution_variables) + '''</td></tr>
                        <tr><td><b>Time: </b></td><td>''' + time.strftime("%d-%b-%y %H:%M") + '</td></tr>'
    options.display.float_format = '{:,.2f}'.format
    table = ""
    for df in results:        # loop through all results of a test
        if isinstance(df, DataFrame):
            table += df.to_html().replace('<table border="1" class="dataframe">','<table class="table table-striped">') #use bootstrap styling
        else:
            table += '<table class="table table-striped">'
            table += markdown.markdown(df)
            table += '</table>'

    footer = '</table>'
    return test_description + table + footer


def generate_html_report(report_title, airline_code, testScript):
    html_header = '''
    <html>
        <head>
            <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css">
            <style>
                body {
                    margin:0 100;
                    background:whitesmoke;
                }
                .comment {
                    font-size: 12pt;
                    font-family: georgia;
                    background-color: linen;
                    color: black;
                    border-color: darkred;
                  border-style: solid;
                  padding: 5p
                }

                .red_b {
                    border: 2px;
                    border-color: red;
                    border-style: solid;
                }
            </style>
        </head>
        <body>'''

    html_title = '<h1>' + report_title + ' ' + airline_code + ' ' + time.strftime("%d-%b-%y %H:%M") + '</h1>'

    html_body = ""
    print("Number of tests: ", len(testScript.all_tests_sql))
    print("Number of results: ", len(testScript.all_test_results))
    for i in range(0, len(testScript.all_tests_sql)):
        print(i)
        html_body += generate_test_html(testScript.all_tests_sql[i], testScript.all_test_results[i].results)
        #for r in testScript.all_test_results[i].results:        # loop through all results of a test
        #    html_body += generate_test_html(testScript.all_tests_sql[i], r)

    html_footer = '</body></html>'

    return html_header + html_title + html_body + html_footer


def generate_intergrity_html(report_title, airline_code, start_date, end_date, source_db, test_db, testScript):
    html_header = '''
    <html>
        <head>
            <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css">
            <style>body{ margin:0 100; background:whitesmoke; }</style>
        </head>
        <body>'''

    html_title = '<h1>' + report_title + ' ' + airline_code + ' ' + time.strftime("%d-%b-%y %H:%M") +'</h1>'
    html_body = '<p>' +"  Execution Period:"+str(time.strftime('%d-%b-%Y',time.strptime(start_date,"%Y%m%d")))+" - "+str(time.strftime('%d-%b-%Y',time.strptime(end_date,"%Y%m%d")))+'</p>'
    html_body += '<p>' +" Source DB:"+str(source_db)+'</p>'
    html_body += '<p>' +" Test DB:"+str(test_db)+'</p>'
    html_body += '''<table height='50' border="0"><br></br></table>'''


    #Sanity tests
    html_body += "<h3> Sanity Tests </h3> "
    html_body += '''<table border="0" ><table style="width: auto;" class="table table-striped">'''

    test_description=""
    failedTests=0

    i=0
    for df in testScript.all_test_results[0].results:
        if not df.empty:
            test_description += '''<tr><td>''' + testScript.all_tests_sql[i].name + '''</td><td>  '''+"  :FAILED ("+str(len(df))+")"+'''</td></tr>'''
            failedTests+=1
        i+=1

    if failedTests==0:
            test_description += '''<tr><td>''' + "All Sanity Tests passed"+ '''</td></tr>'''

    test_description+='''</table>'''

    html_body +=test_description
    html_body += '''<table height='50' border="0"><br></br></table>'''


    #Set report table titles
    html_body +='''<table border="0" ><tr><td><h3>''' + "Booking Stats "+ '''</h3></td><td width="70"></td><td><h3>''' + "Ticket and Coupon Overview          "+ '''</h3></td><td width="70"></td><td><h3>''' + "Revenue Stats"+ '''</h3></td></tr>'''
    html_body+='''<tr valign="top"><td>'''
    html_body += '''<table style="width: auto;" class="table table-striped">'''




    #Bookings overview
    test_description=""

    i=0
    for df in testScript.all_test_results[1].results:
        print(df)
        test_description += '''<tr><td>''' "Total flights" '''</td><td align="right">  '''+format(df['total_flights'][0])+'''</td></tr>'''
        test_description += '''<tr><td>''' + "Total Offline bookings" + '''</td><td align="right">  '''+format(df['total_bif_bookings'][0])+'''</td></tr>'''
        test_description += '''<tr><td>''' + "Total Planitas bookings" + '''</td><td align="right">  '''+format(df['total_planitas_bookings'][0])+'''</td></tr>'''
        test_description += '''<tr><td>''' + "Under reported Flights" + '''</td><td align="right">  '''+format(df['under_reported_flights'][0])+'''</td></tr>'''
        test_description += '''<tr><td>''' + "Under reported Flights PCT" + '''</td><td align="right">  '''+format(df['under_reported_flights_pct'][0])+'''</td></tr>'''
        test_description += '''<tr><td>''' + "Over reported Flights" + '''</td><td align="right">  '''+format(df['over_reported_flights'][0])+'''</td></tr>'''
        test_description += '''<tr><td>''' + "Over reported Flights PCT" + '''</td><td align="right">  '''+format(df['over_reported_flights_pct'][0])+'''</td></tr>'''
        test_description += '''<tr><td>''' + "Exact matches" + '''</td><td align="right">  '''+format(df['exact_matches'][0])+'''</td></tr>'''
        test_description += '''<tr><td>''' + "Exact match PCT" + '''</td><td align="right">  '''+format(df['exact_match_pct'][0])+'''</td></tr>'''
        test_description += '''<tr><td>''' + "PCT difference" + '''</td><td align="right">  '''+format(df['pct_diff'][0])+'''</td></tr>'''
        i+=1

    test_description+='''</table></td><td width="70"></td>'''
    html_body +=test_description


    #Coupon and revenue figures
    html_body += '''<td><table style="width: auto;" class="table table-striped">'''
    test_description=""

    i=0
    for df in testScript.all_test_results[2].results:
        test_description += '''<tr><td>''' "Missing Coupons" '''</td><td align="right">  '''+format(df['missing_coupouns'][0])+'''</td></tr>'''
        test_description += '''<tr><td>''' + "Missing Tickets" + '''</td><td align="right">  '''+format(df['missing_tickets'][0])+'''</td></tr>'''
        test_description += '''<tr><td>''' + "Pct missing coupons" + '''</td><td align="right">  '''+str(round(float(format(df['per_missing_coupons'][0])),2))+'''</td></tr>'''
        test_description += '''<tr><td>''' + "missing revenue" + '''</td><td align="right">  '''+format(df['missing_revenue'][0])+'''</td></tr>'''
        test_description += '''<tr><td>''' + "Accuracy" + '''</td><td align="right">  '''+str(round(float(format(df['accuracy'][0])),2))+'''</td></tr>'''
        i+=1

    test_description+='''</table></td><td width="70"></td>'''

    html_body +=test_description



    #revenue statistics
    html_body += '''<td><table style="width: auto;" class="table table-striped">'''
    test_description=""

    i=0
    for df in testScript.all_test_results[3].results:
        test_description += '''<tr><td>''' "Zero Fare Coupons" '''</td><td align="right">  '''+format(df['pas_zero_fare_coupons'][0])+'''</td></tr>'''
        test_description += '''<tr><td>''' + "Zero Fare Missed Revenue" + '''</td><td align="right">  '''+format(df['pas_zero_fare_missed_revenue'][0])+'''</td></tr>'''
        test_description += '''<tr><td>''' + "Pas less source coupons" + '''</td><td align="right">  '''+format(df['pas_less_source_coupons'][0])+'''</td></tr>'''
        test_description += '''<tr><td>''' + "Pas more source coupons" + '''</td><td align="right">  '''+format(df['pas_more_source_coupons'][0])+'''</td></tr>'''
        test_description += '''<tr><td>''' + "Pas more source revenue" + '''</td><td align="right">  '''+format(df['pas_more_source_revenue'][0])+'''</td></tr>'''
        test_description += '''<tr><td>''' + "Balance:" + '''</td><td align="right">  '''+format(df['coupon_balance'][0])+'''</td></tr>'''
        test_description += '''<tr><td>''' + "Equal Coupons" + '''</td><td align="right">  '''+format(df['equal_coupons'][0])+'''</td></tr>'''
        test_description += '''<tr><td>''' + "Equal Percentage" + '''</td><td align="right">  '''+str(round(float(format(df['equal_coupon_percentage'][0])),2))+'''</td></tr>'''
        test_description += '''<tr><td>''' + "Equal within 5usd" + '''</td><td align="right">  '''+str(round(float(format(df['within_5dollar_pc'][0])),2))+'''</td></tr>'''
        test_description += '''<tr><td>''' + "Equal within 10usd" + '''</td><td align="right">  '''+str(round(float(format(df['within_10dollar_pc'][0])),2))+'''</td></tr>'''
        i+=1

    test_description+='''</table></td></tr></table>'''

    html_body +=test_description


    html_body +='''<p><HR WIDTH="60% SIZE="20" COLOR="green"  ALIGN="LEFT"></p>'''

    #############Database comparison ################################################

    test_description=""

    ###### PNR AND SEGMENT COUNT DIFFERENCES  ########
    #passengers per pnr by creation date
    html_body +='''<table border="0" ><tr><td><h3>''' + "Database Comparison "+ '''</h3></td><td><td><h3>''' + "Fare Analysis "+ '''</h3></td></td></tr>'''
    #html_body += '''<tr><td></td></tr>'''
    html_body+='''<tr valign="top"><td>'''
    #html_body += '''<table style="width: auto;" class="table table-striped"><tr><td><h3>''' + "Database Comparison "+ '''</h3></td></tr>'''
    html_body += '''<table style="width: auto;" class="table table-striped"><th></th><th>''' + "Total "+ '''</th><th>''' + "Total % "+ '''</th></tr>'''


    i=0
    for df in testScript.all_test_results[4].results:
        print(df)
        test_description += '''<tr><td>''' "Pnr Count Difference By Creation Date %" '''</td><td align="right">  '''+format(df['pnr_diff'][0])+'''</td><td align="right">  '''+str(round(float(format(df['pnr_per_diff'][0])),2))+'''</td></tr>'''
        test_description += '''<tr><td>''' "Segment Difference By Creation Date % " '''</td><td align="right">  '''+format(df['pax_seg_diff'][0])+'''</td><td align="right">  '''+str(round(float(format(df['pax_seg_per_diff'][0])),2))+'''</td></tr>'''

        i+=1

    html_body +=test_description


    ###### Coupon count and revenue by issue date ########

    test_description=""

    i=0
    for df in testScript.all_test_results[5].results:
        #print(df)
        test_description += '''<tr><td>''' "Coupon Count Difference By Issue Date %" '''</td><td align="right">  '''+format(df['pax_diff'][0])+'''</td><td align="right">  '''+str(round(float(format(df['pax_per_diff'][0])),2))+'''</td></tr>'''
        test_description += '''<tr><td>''' "revenue Difference By Issue Date % " '''</td><td align="right">  '''+format(df['fare_diff'][0])+'''</td><td align="right">  '''+str(round(float(format(df['fare_per_diff'][0])),2))+'''</td></tr>'''

        i+=1


    html_body +=test_description



    ###### Passenger Counts Difference Per Pnr By Creation Date ########

    test_description=""
    i=0
    for df in testScript.all_test_results[6].results:
        #print(df)
        test_description += '''<tr><td>''' "Passenger Counts Difference Per Pnr By Creation Date % " '''</td><td align="right">  '''+format(df['pax_diff'][0])+'''</td><td align="right">  '''+str(round(float(format(df['pax_per_diff'][0])),2))+'''</td></tr>'''

        i+=1

    html_body +=test_description



    ###### Maureva upadated fares ########
    test_description=""

    i=0
    for df in testScript.all_test_results[7].results:
        #print(df)
        test_description += '''<tr><td>''' "Maureva upadated fares " '''</td><td align="right">  '''+format(df['updated_fares_diff'][0])+'''</td><td align="right">  '''+str(round(float(format(df['updated_fares_per_diff'][0])),2))+'''</td></tr>'''

        i+=1



    test_description+='''</table></td><td width="180"></td>'''
    html_body +=test_description


    ###### FARE ANALYSIS ########
    test_description=""

    html_body += '''<td><table style="width: auto;" class="table table-striped">'''
    #html_body +='''<table border="0" ><tr><td><h3>''' + "Fare Analysis "+ '''</h3></td></tr>'''
    #html_body+='''<tr valign="top"><td>'''
    #html_body += '''<table style="width: auto;" class="table table-striped">'''


    for df in testScript.all_test_results[9].results:
        test_description+=df[['pax_per_diff', 'total_fare_per_diff']].to_html().replace('<table border="1" class="dataframe">','<table class="table table-striped">')


    test_description+='''</table></td></tr></table>'''
    html_body +=test_description

    ###### FARE ANALYSIS END########

    html_body += '''<table height='50' border="0"><br></br></table>'''

    ###### bookings comparison top ########
    html_body +='''<table ><tr><td><h3>''' + "Top Flights By Passenger Count Difference "+ '''</h3></td></tr>'''

    #html_body += '''<td><table style="width: auto;" class="table table-striped">'''
    test_description=""

    for df in testScript.all_test_results[8].results:
        test_description+=df.head(3).to_html().replace('<table border="1" class="dataframe">','<table style="width: 50%;" class="table table-striped">')
        test_description+=df.tail(3).to_html().replace('<table border="1" class="dataframe">','<table style="width: 50%;" class="table table-striped">')

    #test_description+='''</td></tr></table>'''
    test_description+='''</td></tr></table>'''



    html_body +=test_description

    test_description=""




    html_body +=test_description





    html_footer = '</body></html>'

    return html_header + html_title + html_body + html_footer

