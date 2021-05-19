import csv

decision = [0, 1]  # 0 - go to bin, 1 - pick up
levels = [1, 2, 3, 4, 5]
# 1 - 0;20  2 - 20;40  3 - 40;60  4 - 60;80  5 - 80;100
# 1 - 0;40  2 - 40;80  3 - 80;120  4 - 120;160  5 - 160+


def enough_free_space(available_space, trash_size, available_mass, mass_trash):
    if available_space + trash_size <= 5 and available_mass + mass_trash <= 5:
        return True
    return False


def where_is_closer(bin_distance, trash_distance):
    if bin_distance <= trash_distance:
        return 0
    return 1


with open('tree_dataset.csv', 'w', newline='') as csv_file:
    file_writer = csv.writer(csv_file)
    file_writer.writerow(["distance_to_bin", "distance_to_trash", "filling_mass", "filling_space", "trash_mass", "trash_space", "decision"])

    counter = 0

    for distance_to_bin in levels:
        for distance_to_trash in levels:
            for filling_mass in levels:
                for filling_space in levels:
                    for trash_mass in levels:
                        for trash_space in levels:
                            if counter % 10 == 0:
                                if distance_to_bin == 1 and filling_space >= 1 and filling_mass >= 1:
                                    file_writer.writerow([distance_to_bin, distance_to_trash, filling_mass, filling_space, trash_mass, trash_space, 0])
                                elif distance_to_trash == 1 and enough_free_space(filling_space, trash_space, filling_mass, trash_mass):
                                    file_writer.writerow([distance_to_bin, distance_to_trash, filling_mass, filling_space, trash_mass, trash_space, 1])
                                elif filling_mass == 4 or filling_space == 4 and not enough_free_space(filling_space, trash_space, filling_mass, trash_mass):
                                    file_writer.writerow([distance_to_bin, distance_to_trash, filling_mass, filling_space, trash_mass, trash_space, 0])
                                elif filling_mass == 5 or filling_space == 5:
                                    file_writer.writerow([distance_to_bin, distance_to_trash, filling_mass, filling_space, trash_mass, trash_space, 0])
                                elif filling_mass <= 3 and filling_space <= 3 and enough_free_space(filling_space, trash_space, filling_mass, trash_mass):
                                    file_writer.writerow([distance_to_bin, distance_to_trash, filling_mass, filling_space, trash_mass, trash_space, 1])
                                elif filling_mass == 4 or filling_space == 4 and enough_free_space(filling_space, trash_space, filling_mass, trash_mass):
                                    file_writer.writerow([distance_to_bin, distance_to_trash, filling_mass, filling_space, trash_mass, trash_space, where_is_closer(distance_to_bin, distance_to_trash)])
                                elif not enough_free_space(filling_space, trash_space, filling_mass, trash_mass):
                                    file_writer.writerow([distance_to_bin, distance_to_trash, filling_mass, filling_space, trash_mass, trash_space, 0])
                                else:
                                    file_writer.writerow([distance_to_bin, distance_to_trash, filling_mass, filling_space, trash_mass, trash_space, None])

                            counter += 1
