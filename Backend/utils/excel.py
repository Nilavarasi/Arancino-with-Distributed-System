import gspread


def next_available_row(worksheet):
    str_list = list(filter(None, worksheet.col_values(1)))
    return str(len(str_list)+1)


def write_data_in_excel(data):
    sa = gspread.service_account('./creds.json')
    sh = sa.open("sensor data")
    worksheet = sh.worksheet("Sheet1")
    print('Rows: ', worksheet.row_count)
    print('Rows: ', data)
    next_row = next_available_row(worksheet)
    # worksheet.update_acell("A{}".format(next_row), date)
    # worksheet.update_acell("B{}".format(next_row), sensor_data)
    print("next_row, len(data)", next_row, len(data))
    worksheet.update('A{}:B{}'.format(next_row, len(data)+(int(
        next_row)-1)), data)
