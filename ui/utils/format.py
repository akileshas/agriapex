import pandas as pd


def format_schedule_response(response):
    stages = []
    for key, value in response.items():
        stage_name = value[0]
        urea = value[1][0]
        urea_unit = value[1][1]
        dap = value[2][0]
        dap_unit = value[2][1]
        mop = value[3][0]
        mop_unit = value[3][1]
        percentage = value[4]
        start_date = value[5]
        end_date = value[6]

        stages.append([
            key,
            stage_name,
            urea,
            urea_unit,
            dap,
            dap_unit,
            mop,
            mop_unit,
            percentage,
            start_date,
            end_date
        ])

    df = pd.DataFrame(stages, columns=[
        "Stage", "Stage Name", "Urea", "Urea Unit", "DAP", "DAP Unit",
        "MOP", "MOP Unit", "Percentage", "Start Date", "End Date"
    ])

    return df
