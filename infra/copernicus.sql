select time,bbp,cdm from athena_clean_data_db.biogeochemicaloptics
where (lat between 26.14999999957532 and  26.809166322814903)
and (lon between -113.89444399967512  and -113.26666699967019 )

select time,pico,prokar,chl,dino,hapto,green,prochlo,nano,
diato,micro from athena_clean_data_db.plankton
where (lat between 26.14999999957532 and  26.809166322814903)
and (lon between -113.89444399967512  and -113.26666699967019 )

select time, rrs670, rrs412, rrs555, rrs443 from athena_clean_data_db.reflectance  
where (lat between 26.14999999957532 and  26.809166322814903)
and (lon between -113.89444399967512  and -113.26666699967019 )


select time, analysed_sst from athena_clean_data_db.seasurfacetemperature
where (lat between 26.14999999957532 and  26.809166322814903)  
where (lat between 26.14999999957532 and  26.809166322814903)
and (lon between -113.89444399967512  and -113.26666699967019 )


select time,spm, kd490, zsd from athena_clean_data_db.transparence
where (lat between 26.14999999957532 and  26.809166322814903)
and (lon between -113.89444399967512  and -113.26666699967019 )


select time, vo, uo from athena_clean_data_db.totalsurfaceaand15mcurrent
where (latitude between 26.14999999957532 and  26.809166322814903)
and (longitude between -113.89444399967512  and -113.26666699967019 )
