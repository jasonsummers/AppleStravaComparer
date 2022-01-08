import os
import csv
import shutil

if __name__ == '__main__':
    apple_routes_dir = "/path/to/apple_health_export/workout-routes"
    apple_route_files = os.listdir(apple_routes_dir)
    apple_route_start_times = []
    strava_activities_file = "/path/to/strava_export/activities.csv"
    strava_activity_start_times = []
    gpx_manual_upload_dir = "/path/to/missing_activity_output_directory/"

    from dateutil import parser
    date_format = "%Y-%m-%d %H:%M"

    for route in apple_route_files:
        filepath = apple_routes_dir + '/' + route

        from lxml import etree
        gpx = etree.parse(filepath)
        start_time = gpx.xpath("//gpx:time", namespaces = {'gpx': "http://www.topografix.com/GPX/1/1"})[1].text
        x = {
            "filename": route,
            "starttime": parser.parse(start_time).strftime(date_format),
            "filepath": filepath
        }
        apple_route_start_times.append(x)

    with open(strava_activities_file) as activities_csv:
        csv_reader = csv.reader(activities_csv, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count = line_count + 1
            else :
                strava_activity_start_times.append(parser.parse(row[1]).strftime(date_format))

    for apple_route in apple_route_start_times:
        if apple_route["starttime"] not in strava_activity_start_times :
            shutil.copy(apple_route["filepath"], gpx_manual_upload_dir + apple_route["filename"])
