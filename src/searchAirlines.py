# -*- coding: utf-8 -*-

import sys
from workflow import Workflow3, web
from workflow.background import is_running
from downloadDataFiles import string_from_percent, build_wf_entry


# Airlines with autolookup

# Data source: https://raw.githubusercontent.com/jpatokal/openflights/master/data/airlines.dat

def main(wf):
    query = str(wf.args[0]).lower()
    log.debug(query)

    code_match = []
    name_match = []
    other_match = []

    import os.path
    if not os.path.exists('airlines.csv'):
        if is_running('bg'):
            pct = None
            while pct is None:
                try:
                    pct = wf.stored_data('download_percent')
                except:
                    pass

            progress = wf.stored_data('download_progress')
            file = wf.stored_data('download_file')

            wf.rerun = 0.5

            title = "Please wait for data file downloads to complete"
            subtitle = progress + " " + string_from_percent(pct) + " " + str(pct) + "%"
            wf.add_item(title, subtitle=subtitle)
        else:
            wf.add_item('No data files', 'Run "aptinit" to get airline database', icon="images/evil.png", arg="airline_init")

        wf.send_feedback()
        return

    with open('airlines.csv', 'r') as airport_file:
        for line in airport_file:
            line = line.rstrip('\n')
            if query in line.lower():

                parts = line.split(',')
                airline_id = parts[0].replace('"', '')
                name = parts[1].replace('"', '')
                alias = parts[2].replace('"', '')
                iata_code = "IATA: " + parts[3].replace('"', '')
                icao_code = "ICAO: " + parts[4].replace('"', '')
                callsign = parts[5].replace('"', '')
                country = parts[6].replace('"', '')
                active = parts[7].replace('"', '')

                # print(airline_id, iata_code, icao_code, name, alias, callsign, country, active)
                codes = filter(None, {icao_code, iata_code})

                # print name, codes
                # \\U0001F1F2\\U0001F1FD\\U0000FE0F

                subtitle = ", ".join(codes)

                title = str(name).decode('utf-8', 'ignore')
                arg = icao_code
                valid = 'True'

                value_map = {'subtitle': subtitle, 'title': title, 'arg': arg, 'valid': valid}
                if any(filter(lambda x: query.upper() in x, codes)):
                    code_match.append(value_map)
                elif query.upper() in name.upper():
                    name_match.append(value_map)
                else:
                    other_match.append(value_map)

        # Build ordered search results
        for i in code_match:
            wf.add_item(**i)
        for i in name_match:
            wf.add_item(**i)
        for i in other_match:
            wf.add_item(**i)

    wf.send_feedback()


if __name__ == u"__main__":
    wf = Workflow3()
    log = wf.logger
    sys.exit(wf.run(main))
