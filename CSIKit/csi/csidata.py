from CSIKit.csi.csiframe import CSIFrame
from CSIKit.csi.csimetadata import CSIMetadata
from CSIKit.util.csitools import get_CSI

class CSIData:

    def __init__(self, filename: str="", chipset: str=""):
        
        self.frames = []
        self.timestamps = []

        self.expected_frames = 0
        self.skipped_frames = 0

        self.bandwidth = 0

        self.filename = filename
        self.chipset = chipset

    def set_chipset(self, chipset: str):
        self.chipset = chipset

    def push_frame(self, frame: CSIFrame):
        self.frames.append(frame)

    def get_metadata(self) -> CSIMetadata:
        chipset = self.chipset

        bandwidth = self.bandwidth

        unmodified_csi_matrix = self.frames[0].csi_matrix
        _, no_frames, no_subcarriers = get_CSI(self)

        rx_count = (0, 0)
        tx_count = (0, 0)

        if len(unmodified_csi_matrix.shape) <= 2:
            rx_count, tx_count = (1, 1)
        elif len(unmodified_csi_matrix.shape) == 3:
            rx_count, tx_count = unmodified_csi_matrix.shape[1:]

        antenna_config_string = "{} Rx, {} Tx".format(rx_count, tx_count)

        timestamps = self.timestamps
        final_timestamp = timestamps[-1]

        #Check if timestamp is relative or epoch.

        time_length = 0
        if len(str(final_timestamp)) > 9:
            #Likely an epoch timestamp.
            #Get diff between first and last.
            time_length = final_timestamp - timestamps[0]
        else:
            time_length = float(final_timestamp)

        if final_timestamp == 0:
            average_sample_rate = 0
        else:
            average_sample_rate = no_frames/time_length

        data = {
            "chipset": chipset,
            "bandwidth": bandwidth,
            "antenna_config": antenna_config_string,
            "frames": no_frames,
            "subcarriers": no_subcarriers,
            "time_length": time_length,
            "average_sample_rate": average_sample_rate,
            "csi_shape": unmodified_csi_matrix.shape
        }    

        return CSIMetadata(data)