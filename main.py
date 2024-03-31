from collusion import get_collusion_tva_result
from tva_io import parse_args, write_to_output
from voting import get_basic_tva_result

if __name__ == "__main__":
    mode, system_preferences, schemes, collusion_groups, output_file, runoff_elections, runoff_output_file = parse_args()

    output_file = "output.json"
    runoff_output_file = "runoff_output.json"

    if mode == 'basic':
        tva_result = get_basic_tva_result(system_preferences, schemes)
        write_to_output(tva_result, output_file)
    elif mode == 'collusion':
        tva_result = get_collusion_tva_result(system_preferences, schemes, collusion_groups)
        write_to_output(tva_result, output_file)
    elif mode == 'runoff':
        if runoff_elections > 1:
            basic_tva_result, result = get_basic_tva_result(system_preferences, schemes, runoff=runoff_elections)
            write_to_output(basic_tva_result, runoff_output_file)
            for pref in system_preferences:
                temp = []
                for val in pref:
                    if val in result[:runoff_elections]:
                        temp.append(val)
                system_preferences[system_preferences.index(pref)] = temp

        if runoff_elections > 0:
            tva_result = get_basic_tva_result(system_preferences, schemes)