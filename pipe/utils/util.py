import csv


class Util:

    @staticmethod
    def dict_to_csv(dict_data, headers, filename):
        with open(filename, 'w', newline='\n') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers, dialect='excel')
            writer.writeheader()
            writer.writerows(dict_data)
