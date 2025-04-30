from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import StreamingResponse
import pandas as pd
import numpy as np
import math
import os
from datetime import datetime

app = FastAPI()

# Path to the CSV file where events will be stored
events_file = "events.csv"

# Helper function to determine the column names for each "r"
def get_column_names_from_r(r_value):
    """
    Esta función devuelve el nombre de las columnas dinámicas basadas en el valor de "r".
    Se puede adaptar según las necesidades de los datos.
    """ 
    if r_value == 774:
        # Para r=774, generamos columnas para cada bit procesado
        return [f"data_{r_value}_bit_{i+1}" for i in range(10)]
    if r_value >= 2049:
        return [f"data_{r_value}_bit_{i+1}" for i in range(4)]
    else:
        # Para otros valores de r, mantener las columnas originales
        return [f"data_{r_value}_v", f"data_{r_value}_lat", f"data_{r_value}_long"]
# Function to process the 'v' value, assuming some might have additional columns
def process_v_value(v_value, r_value):
    """
    Procesa el valor de 'v'. Si 'v' tiene más de una columna (por ejemplo, una lista o
    un valor que debe dividirse), lo maneja aquí.
    """
    print(f"procesando valor  v_value: {v_value} for r_value: {r_value}")
    print(r_value)
    print(type(r_value))
    if r_value == 774:
        print("#############################")
        # tranformamos el valor de a bits, y los separamos en una lista cada valor de bit en total es un numero de 16 bits        
        v_bit = format(v_value, '016b')  # Convertimos a binario y rellenamos con ceros a la izquierda
        # Retornamos una lista de 16 elementos, cada uno representando un bit
        print(f"Transformed v_value: {v_value} for r_value: {r_value}")
        #  imprimimos los bits del 7 al 16
        v_bit = [int(bit) for bit in v_bit[6:]]  # Convertimos cada bit a entero y tomamos del 7 al 16
        print(v_bit)
        print(f" v_bit procesado: {v_bit} for r_value: {r_value}")
        return v_bit  # Retorna la lista de bits
    if r_value >= 2049:
        print("---------------------------------")
        v_bit = format(v_value, '016b')  # Convertimos a binario y rellenamos con ceros a la izquierda
        # separamos los resultados en numeros de 4 bits, emepzando desde el bit 1 hasta el 16
        # convertimos cada 4 bits a un numero entero
        v_bit = [int(v_bit[i:i+4], 2) for i in range(0, 16, 4)]  # Convertimos cada grupo de 4 bits a entero
        print(f"Transformed v_value: {v_value} for r_value: {r_value}")
        print(v_bit)
        return v_bit  # Retorna la lista de bits
        
        

    if isinstance(v_value, list):
        # Si v es una lista, podemos crear varias columnas
        return v_value  # Retorna la lista como tal, que luego se asigna a las columnas
    else:
        # Si 'v' es un valor simple, solo lo retornamos en forma de lista
        return [v_value]

@app.on_event("startup")
async def startup_event():
    # Ensure the CSV exists (with headers) on startup
    if not os.path.exists(events_file) or os.stat(events_file).st_size == 0:
        # Initialize the file with headers if it does not exist or is empty
        df = pd.DataFrame(columns=["site", "controller", "company", "received_at", "lat", "long","extended_excep_code", "modem_mode","manuifacturer_code","model_numbre","serial_number","serial_number_2","control_mode","control_shutdown_alarm","no_font_file","satellite_telemetry_alarm","telemetry_alarm","warning_alarm_active","electrical_trip","shutdown_alarm_active","control_unit_failure","unimplemented","control_unit_not_configured","oil_pressure"," coolant_temp","oil_temp","fuel_level","charge_alternator_volt","engine_battery_volt","engine_speed","generator_frequency","generator_L1_N_volt","generator_L2_N_volt","generator_L3_N_volt","generator_L1_L2_volt","generator_L2_L3_volt","generator_L1_L3_volt","generator_L1_current","generator_L2_current","generator_L3_current","generator_L1_watts","generator_L2_watts","generator_L3_watts","mains_frequency","main_L1_N_volt","main_L2_N_volt","main_L3_N_volt","main_L1_L2_volt","main_L2_L3_volt","main_L1_L3_volt",
        "generator_phase_rotation","mains_phase_ratation","main_L1_current","main_L2_current","main_L3_current","named_alarms","emergency_stop","low_oil_pressure","high_coolant_temperature","high_oil_temperature","under_speed","over_speed","fail_to_start","fail_to_come_to_rest","loss_of_speed_sensing","generator_low_voltage","generator_high_voltage","generator_low_frequency","generator_high_frequency","generator_high_current","generator_earth_fault","generator_reverse_power","air_flap","oil_pressure_sender_fault","coolant_temperature_sender_fault","oil_temperature_sender_fault","fuel_level_sender_fault","magnetic_pickup_fault","loss_of_ac_speed_signal","charge_alternator_failure","low_battery_voltage","high_battery_voltage","low_fuel_level","high_fuel_level","generator_failed_to_close","mains_failed_to_close","generator_failed_to_open","mains_failed_to_open","mains_low_voltage","mains_high_voltage","bus_failed_to_close","bus_failed_to_open","mains_low_frequency","mains_high_frequency","mains_failed", "mains_phase_rotation_wrong", "generator_phase_rotation_wrong", "maintenance_due", "clock_not_set", "local_lcd_configuration_lost", "local_telemetry_configuration_lost", "control_unit_not_calibrated", "modem_power_fault", "generator_short_circ", "failure_to_synchronise", "bus_live", "scheduled_ran", "bus_phase_rotation_wrong", "priority_selection_error", "multiset_communications_msc_data_error", "multiset_communications_msc_id_error", "multiset_communications_msc_failure", "multiset_communications_msc_too_few_sels", "multiset_communications_msc_alarms_inhibited", "multiset_communications_msc_old_version_units", "mains_reverse_power", "minimum_sets_not_reached", "insufficient_capacity_available", "expansion_input_unit_not_calibrated", "expansion_input_unit_failure", "auxiliary_sender_1_low", "auxiliary_sender_1_high", "auxiliary_sender_1_fault", "auxiliary_sender_2_low", "auxiliary_sender_2_high", "auxiliary_sender_2_fault", "auxiliary_sender_3_low", "auxiliary_sender_3_high", "auxiliary_sender_3_fault", "auxiliary_sender_4_low", "auxiliary_sender_4_high", "auxiliary_sender_4_fault", "engine_control_unit_ecu_link_lost", "engine_control_unit_ecu_failure", "engine_control_unit_ecu_error", "low_coolant_temperature", "out_of_sync", "low_oil_pressure_switch", "alternative_auxiliary_mains_fail", "loss_of_excitation", "mains_kw_limit", "negative_phase_sequence", "mains_rocof", "mains_vector_shift", "mains_g59_low_frequency", "mains_g59_high_frequency", "mains_g59_low_voltage", "mains_g59_high_voltage", "mains_g59_trip", "generator_kw_overload", "engine_inlet_temperature_high", "bus_1_live", "bus_1_phase_rotation_wrong","bus_2_live","bus_2_phase_rotation_wrong","reserved"
])
        df.to_csv(events_file, index=False)

@app.post("/events")
async def receive_event(request: Request):
    try:
        payload = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON payload")

    # Initialize a row with fixed columns and lat/long
    row = {
        "site": payload["site"],
        "controller": payload["controller"],
        "company": payload["company"],
        "received_at": datetime.utcnow().isoformat() + "Z",  # Timestamp in UTC
        "lat": 0,  # Initialize lat and long as None
        "long": 0
    }

    # Store the latitude and longitude once for the whole event
    if "lat" in payload:
        row["lat"] = payload["lat"]
    if "long" in payload:
        row["long"] = payload["long"]

    # Maintain the headers for dynamic columns (columns like data_<r>_v)
    dynamic_columns = []

    # Add dynamic columns based on each "r" value
    for item in payload["data"]:
        # Generate dynamic column names for each r
        dynamic_column = get_column_names_from_r(item["r"])

        # Add to dynamic columns list
        dynamic_columns.extend(dynamic_column)

        # Process the 'v' value (in case it contains more than one piece of information)
        processed_v = process_v_value(item.get("v", None), item["r"])
        
        # Assign the processed 'v' to the respective dynamic columns (handling multi-column values)
        for idx, value in enumerate(processed_v):
            row[dynamic_column[idx]] = value

    # Convert to DataFrame and append to CSV
    df = pd.DataFrame([row])  # Ensure we only create one row

    # Ensure the CSV contains the headers if it's the first time writing to it
    file_exists_and_not_empty = os.path.exists(events_file) and os.stat(events_file).st_size > 0

    df.to_csv(
        events_file,
        mode="a",  # Append mode
        header=not file_exists_and_not_empty,  # Write header only if the file is empty
        index=False
    )

    return {"status": "success", "received_at": row["received_at"]}


@app.get("/events/csv")
async def get_events_csv():
    # Return the raw CSV file
    if not os.path.exists(events_file):
        raise HTTPException(status_code=404, detail="Events file not found")
    
    def iterfile():
        with open(events_file, mode="r", encoding="utf-8") as f:
            for line in f:
                yield line
    
    return StreamingResponse(iterfile(), media_type="text/csv")

def clean_json_values(df):
    """Limpia valores no compatibles con JSON (inf, -inf, NaN)"""
    # Reemplaza inf/-inf con None (que se convierte en null en JSON)
    df = df.replace([np.inf, -np.inf], None)
    # Reemplaza NaN con None
    df = df.replace({math.nan: None})
    return df

@app.get("/events")
async def get_events():
    # Return all events as JSON
    try:
        df = pd.read_csv(events_file)
        # Limpia valores no compatibles con JSON
        df = clean_json_values(df)
        records = df.to_dict(orient="records")
        return {"events": records}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not read events file: {str(e)}")

@app.get("/events/{company_name}")
async def get_events_by_company(company_name: str):
    # Filtrar eventos por la empresa
    try:
        df = pd.read_csv(events_file)
        company_events = df[df['company'] == company_name]
        
        # Limpia valores no compatibles con JSON
        company_events = clean_json_values(company_events)
        records = company_events.to_dict(orient="records")
        
        if not records:
            raise HTTPException(status_code=404, detail="No events found for this company")

        return {"events": records}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not read events file: {str(e)}")

@app.get("/events/latest/{company_name}")
async def get_latest_event_by_company(company_name: str):
    # Obtener el último evento registrado para una empresa
    try:
        df = pd.read_csv(events_file)
        company_events = df[df['company'] == company_name]
        
        if company_events.empty:
            raise HTTPException(status_code=404, detail="No events found for this company")

        # Ordenar por la fecha de recepción (received_at) y tomar el último
        latest_event = company_events.sort_values("received_at", ascending=False).iloc[0]
        
        # Limpia valores no compatibles con JSON
        latest_event = latest_event.replace([np.inf, -np.inf, math.nan], None)
        
        return {"latest_event": latest_event.to_dict()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not read events file: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000,)
