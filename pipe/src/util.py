import csv


class Util:

    # Writes result set to csv. Takes a list of dictionaries: one per message
    @staticmethod
    def write_object_to_csv(list_dict_data, filename):
        with open(filename, 'w', newline='\n') as csvfile:

            headers = list(list_dict_data[0].get_values().keys())
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writeheader()

            try:
                for i in list_dict_data:
                    writer.writerow(i.get_values())
            except AttributeError as error:
                print(error.__repr__())
