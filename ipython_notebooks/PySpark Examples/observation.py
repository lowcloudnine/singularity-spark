import datetime
import string

class Observation(object):
    """ A weather observation from the GSOD data set. """
    def __init__(self):
        self = None
     
    def injest(self, ob):
        """ Takes in a string observation in the GSOD format and populates 
        the observation with actual data.
        
        """
        ob = ob.split()
        for element in ob:
            if element[-1] not in string.digits:
                ob[ob.index(element)] = element[:-1]
        self.stn_id = str(ob[0])
        self.wban = str(ob[1])
        self.year = int(ob[2][:4])
        self.month = int(ob[2][4:6])
        self.day = int(ob[2][6:])
        self.mean_tmp = float(ob[3])
        self.num_of_obs = int(ob[4])
        self.mean_dwpt = float(ob[5])
        self.slp = float(ob[7])
        self.stp = float(ob[9])
        self.vsby = float(ob[11])
        self.wnd_spd = float(ob[13])
        self.max_wnd_spd = float(ob[15])
        self.gust = float(ob[16])
        self.max_tmp = float(ob[17])
        self.min_tmp = float(ob[18])
        self.precip = float(ob[19])
        self.sn_dpth = float(ob[20])
        self.frshtt = str(ob[21])
        
    def __repr__(self):
        display = []
        
        display.append("{:<20}{:>20}".format(
                "Station Id:  {}".format(self.stn_id),
                "Number of Obs: {}".format(self.num_of_obs)
        ))
        display.append("-" * 40)
        display.append("{:>40}".format("{:}-{:}-{:}"\
                       .format(self.year, self.month, self.day)))
        display.append("Min Temperature:      {:>5.1f}".format(self.min_tmp))
        display.append("Mean Temperature:     {:>5.1f}".format(self.mean_tmp))
        display.append("Max Temperature:      {:>5.1f}".format(self.max_tmp))
                
        return "\n" + "\n".join(display) + "\n"
    
    def get_temps(self):
        """ Returns a list of the temperatures of the observation in the form
        [min_tmp, mean_tmp, max_tmp]
        
        """
        return [self.min_tmp, self.mean_tmp, self.max_tmp]
    