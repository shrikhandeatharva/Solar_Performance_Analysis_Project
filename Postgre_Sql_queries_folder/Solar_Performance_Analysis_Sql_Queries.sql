-- Query 1
SELECT sm.site_name AS site, 
       SUM(sd.energy_sum) AS total_energy
FROM site_metadata sm
LEFT JOIN (
    SELECT 1 AS site_id, "indregTC1_Energy_kWh_sum" AS energy_sum FROM solar_data_site1
    UNION ALL
    SELECT 2 AS site_id, "indregTC2_Energy_kWh_sum" AS energy_sum FROM solar_data_site2
    UNION ALL
    SELECT 3 AS site_id, "indregTC3_Energy_kWh_sum" AS energy_sum FROM solar_data_site3
) sd ON sm.site_id = sd.site_id
GROUP BY sm.site_name
ORDER BY sm.site_name;


--Query 2 Average power factor of all sites
SELECT sm.site_name AS site,
       AVG(sd.power_factor_avg) AS avg_power_factor
FROM site_metadata sm
LEFT JOIN (
    SELECT 1 AS site_id, "indregTC1_Power_Factor_avg_avg" AS power_factor_avg FROM solar_data_site1
    UNION ALL
    SELECT 2 AS site_id, "indregTC2_Power_Factor_avg_avg" AS power_factor_avg FROM solar_data_site2
    UNION ALL
    SELECT 3 AS site_id, "indregTC3_Power_Factor_avg_avg" AS power_factor_avg FROM solar_data_site3
) sd ON sm.site_id = sd.site_id
GROUP BY sm.site_name
ORDER BY sm.site_name;


-- Query 3: Voltage stability (standard deviation) of all sites
SELECT sm.site_name AS site,
       STDDEV(sd.voltage_avg) AS voltage_stability
FROM site_metadata sm
LEFT JOIN (
    SELECT 1 AS site_id, "indregTC1_Voltage_LL_V_avg" AS voltage_avg FROM solar_data_site1
    UNION ALL
    SELECT 2 AS site_id, "indregTC2_Voltage_LL_V_avg" AS voltage_avg FROM solar_data_site2
    UNION ALL
    SELECT 3 AS site_id, "indregTC3_Voltage_LL_V_avg" AS voltage_avg FROM solar_data_site3
) sd ON sm.site_id = sd.site_id
GROUP BY sm.site_name
ORDER BY sm.site_name;


-- Query 4: Total power output from all sites
SELECT sm.site_name AS site,
       SUM(sd.power_avg) AS total_power_output
FROM site_metadata sm
LEFT JOIN (
    SELECT 1 AS site_id, "indregTC1_Power_kW_avg" AS power_avg FROM solar_data_site1
    UNION ALL
    SELECT 2 AS site_id, "indregTC2_Power_kW_avg" AS power_avg FROM solar_data_site2
    UNION ALL
    SELECT 3 AS site_id, "indregTC3_Power_kW_avg" AS power_avg FROM solar_data_site3
) sd ON sm.site_id = sd.site_id
GROUP BY sm.site_name
ORDER BY sm.site_name;



-- Query 5: Average current from all sites
SELECT sm.site_name AS site,
       AVG(sd.current_avg) AS avg_current
FROM site_metadata sm
LEFT JOIN (
    SELECT 1 AS site_id, "indregTC1_Current_A_avg" AS current_avg FROM solar_data_site1
    UNION ALL
    SELECT 2 AS site_id, "indregTC2_Current_A_avg" AS current_avg FROM solar_data_site2
    UNION ALL
    SELECT 3 AS site_id, "indregTC3_Current_A_avg" AS current_avg FROM solar_data_site3
) sd ON sm.site_id = sd.site_id
GROUP BY sm.site_name
ORDER BY sm.site_name;



-- Query 6: Min and Max voltage from all sites
SELECT sm.site_name AS site,
       MIN(sd.voltage_avg) AS min_voltage,
       MAX(sd.voltage_avg) AS max_voltage
FROM site_metadata sm
LEFT JOIN (
    SELECT 1 AS site_id, "indregTC1_Voltage_LL_V_avg" AS voltage_avg FROM solar_data_site1
    UNION ALL
    SELECT 2 AS site_id, "indregTC2_Voltage_LL_V_avg" AS voltage_avg FROM solar_data_site2
    UNION ALL
    SELECT 3 AS site_id, "indregTC3_Voltage_LL_V_avg" AS voltage_avg FROM solar_data_site3
) sd ON sm.site_id = sd.site_id
GROUP BY sm.site_name
ORDER BY sm.site_name;



-- Query 7: Average reactive power of all sites
SELECT sm.site_name AS site,
       AVG(sd.reactive_power_avg) AS avg_reactive_power
FROM site_metadata sm
LEFT JOIN (
    SELECT 1 AS site_id, "indregTC1_Reactive_Power_kVAR_avg" AS reactive_power_avg FROM solar_data_site1
    UNION ALL
    SELECT 2 AS site_id, "indregTC2_Reactive_Power_kVAR_avg" AS reactive_power_avg FROM solar_data_site2
    UNION ALL
    SELECT 3 AS site_id, "indregTC3_Reactive_Power_kVAR_avg" AS reactive_power_avg FROM solar_data_site3
) sd ON sm.site_id = sd.site_id
GROUP BY sm.site_name
ORDER BY sm.site_name;



-- Query 8: Average phase-wise power for all sites
SELECT sm.site_name AS site,
       AVG(sd.phase_a_power) AS avg_phase_a_power,
       AVG(sd.phase_b_power) AS avg_phase_b_power,
       AVG(sd.phase_c_power) AS avg_phase_c_power
FROM site_metadata sm
LEFT JOIN (
    SELECT 1 AS site_id, "indregTC1_Power_A_kW_avg" AS phase_a_power,
                          "indregTC1_Power_B_kW_avg" AS phase_b_power,
                          "indregTC1_Power_C_kW_avg" AS phase_c_power
    FROM solar_data_site1
    UNION ALL
    SELECT 2 AS site_id, "indregTC2_Power_A_kW_avg" AS phase_a_power,
                          "indregTC2_Power_B_kW_avg" AS phase_b_power,
                          "indregTC2_Power_C_kW_avg" AS phase_c_power
    FROM solar_data_site2
    UNION ALL
    SELECT 3 AS site_id, "indregTC3_Power_A_kW_avg" AS phase_a_power,
                          "indregTC3_Power_B_kW_avg" AS phase_b_power,
                          "indregTC3_Power_C_kW_avg" AS phase_c_power
    FROM solar_data_site3
) sd ON sm.site_id = sd.site_id
GROUP BY sm.site_name
ORDER BY sm.site_name;


-- Query 9: Energy utilization efficiency
SELECT sm.site_name AS site,
       (SUM(sd.energy_sum) / SUM(sd.power_avg)) AS energy_utilization_efficiency
FROM site_metadata sm
LEFT JOIN (
    SELECT 1 AS site_id, "indregTC1_Energy_kWh_sum" AS energy_sum, "indregTC1_Power_kW_avg" AS power_avg FROM solar_data_site1
    UNION ALL
    SELECT 2 AS site_id, "indregTC2_Energy_kWh_sum" AS energy_sum, "indregTC2_Power_kW_avg" AS power_avg FROM solar_data_site2
    UNION ALL
    SELECT 3 AS site_id, "indregTC3_Energy_kWh_sum" AS energy_sum, "indregTC3_Power_kW_avg" AS power_avg FROM solar_data_site3
) sd ON sm.site_id = sd.site_id
GROUP BY sm.site_name
ORDER BY sm.site_name;



-- Query 10: Hourly energy generated by all sites
SELECT sm.site_name AS site,
       sd.hour,
       SUM(sd.hourly_energy) AS hourly_energy
FROM site_metadata sm
LEFT JOIN (
    SELECT 1 AS site_id, DATE_PART('hour', "indregTC1_timestamp") AS hour, "indregTC1_Energy_kWh_sum" AS hourly_energy FROM solar_data_site1
    UNION ALL
    SELECT 2 AS site_id, DATE_PART('hour', "indregTC2_timestamp") AS hour, "indregTC2_Energy_kWh_sum" AS hourly_energy FROM solar_data_site2
    UNION ALL
    SELECT 3 AS site_id, DATE_PART('hour', "indregTC3_timestamp") AS hour, "indregTC3_Energy_kWh_sum" AS hourly_energy FROM solar_data_site3
) sd ON sm.site_id = sd.site_id
GROUP BY sm.site_name, sd.hour
ORDER BY sm.site_name, sd.hour;



