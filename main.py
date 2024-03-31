from collusion import get_collusion_tva_result
from tva_io import parse_args, write_to_output
from voting import get_basic_tva_result

if __name__ == "__main__":
    system_preferences, schemes, collusion_groups, output_file = parse_args()

    output_file = "output.json"
    runoff_output_file = "runoff_output.json"
    runoff_election = 0

    if runoff_election > 1:
       basic_tva_result, result = get_basic_tva_result(system_preferences, schemes, runoff=runoff_election)
       write_to_output(basic_tva_result, runoff_output_file)
       for pref in system_preferences:
           temp = []
           for val in pref:
               if val in result[:runoff_election]:
                   temp.append(val)
           system_preferences[system_preferences.index(pref)] = temp


    if runoff_election > 0:
        tva_result = get_basic_tva_result(system_preferences, schemes)
    elif collusion_groups: # collusion tva
        tva_result = get_collusion_tva_result(system_preferences, schemes, collusion_groups)
    else: # basic tva
        tva_result = get_basic_tva_result(system_preferences, schemes)

    write_to_output(tva_result, output_file)