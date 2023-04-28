from pyedflib import highlevel
import datetime
from brainflow.data_filter import DataFilter
from brainflow import  DataFilter, DetrendOperations, WindowOperations
from brainflow.data_filter import FilterTypes
import numpy as np
class EEGSAVEDATA(object):
    def __init__(self):
        super(EEGSAVEDATA, self).__init__()
        print('inint')
        self.name = 'name'
    
    def saveFile(self,fileName, data, channels, sampleRate, otherInfo):
        # try:
            """
            A convenience function to create an EDF header (a dictionary) that
            can be used by pyedflib to update the main header of the EDF

            Parameters
            ----------
            technician : str, optional
                name of the technician. The default is ''.
            recording_additional : str, optional
                comments etc. The default is ''.
            patientname : str, optional
                the name of the patient. The default is ''.
            patient_additional : TYPE, optional
                more info about the patient. The default is ''.
            patientcode : str, optional
                alphanumeric code. The default is ''.
            equipment : str, optional
                which system was used. The default is ''.
            admincode : str, optional
                code of the admin. The default is ''.
            gender : str, optional
                gender of patient. The default is ''.
            startdate : datetime.datetime, optional
                startdate of recording. The default is None.
            birthdate : str/datetime.datetime, optional
                date of birth of the patient. The default is ''.
            """
            data = data.T
            signals = []
            for channel in range(len(data)):
                DataFilter.detrend(data[channel], DetrendOperations.NO_DETREND.value)
                signals.append(data[channel]/1)
            signals = np.ascontiguousarray(np.array(signals))
            channel_names = channels
            list_of_labels = []
            for i in range(len(channel_names)):
                list_of_labels.append(str(channel_names[i]))
            signalHeaders = highlevel.make_signal_headers(
                list_of_labels=list_of_labels,
                sample_frequency=sampleRate, 
                sample_rate=sampleRate,
                physical_max=187500,
                physical_min=-187500,
                digital_max= 187500,
                digital_min= -187500
            )
            technician = ''
            recording_additional = ''
            patientname = ''
            patient_additional = ''
            patientcode = ''
            equipment = ''
            admincode = ''
            gender = ''
            # birthdate= datetime.datetime(1900, 1, 1).strftime('%d %b %Y')
            keys = list(otherInfo.keys())
            if 'technician' in keys:
                technician = otherInfo["technician"]
            if 'recording_additional' in keys:
                recording_additional = otherInfo['recording_additional']
            if 'patientname' in keys:
                patientname = otherInfo['patientname']
            if 'patient_additional' in keys:
                patient_additional = otherInfo['patient_additional']
            if 'patientcode' in keys:
                patientcode = otherInfo['patientcode']
            if 'equipment' in keys:
                equipment = otherInfo['equipment']
            if 'admincode' in keys:
                admincode=otherInfo['admincode']
            # if 'birthdate' in keys:
            #     birthdate = otherInfo['birthdate']
            header = highlevel.make_header(technician=technician, 
                                        recording_additional=recording_additional,
                                        patientname=patientname,
                                        patient_additional=patient_additional, 
                                        patientcode=patientcode, 
                                        equipment=equipment, 
                                        admincode=admincode,
                                        gender=gender)
            print(signals.shape, len(signalHeaders))
            res = highlevel.write_edf(fileName, signals=signals, signal_headers=signalHeaders, digital=False,file_type=3, header=header)
        # except Exception as e :
        #     print(e)
            