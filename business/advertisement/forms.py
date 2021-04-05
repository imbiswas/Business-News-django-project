from django import forms
from .models import Ads
from bootstrap_datepicker_plus import DateTimePickerInput
from datetime import datetime, timedelta

# To get a list of dates
def perdelta(start, end, delta):
    curr = start
    while curr <= end:
        yield curr
        curr += delta
    

class PostForm(forms.ModelForm):
    class Meta:
        model = Ads
        fields = ['company_name', 'image', 'ad_position', 'duration_start', 'duration_end', 'url']
        widgets = {
            'duration_start' : DateTimePickerInput(format='%Y-%m-%d HH:mm:ss'),
            'duration_end' : DateTimePickerInput(format='%Y-%m-%d HH:mm:ss'),
        }
    
    def clean(self):
        cleaned_data = super(PostForm, self).clean()
        duration_start = cleaned_data['duration_start']
        duration_end = cleaned_data['duration_end']
        ad_position = cleaned_data['ad_position']

        # check for all ads whose End Dates > this news Start Date and Start Dates < this news End Date
        # because that is where the overlapping might occur
        ads = Ads.objects.filter(duration_start__lte=duration_end,duration_end__gte=duration_start, ad_position = ad_position)

        # n is the number of ads for each ad_position
        # n denotes the limit of ads that can be in each position
        # COntent may be 5, header may be 6 ads per header and so on
        if ad_position == 'H': 
            n = 3
        elif ad_position == 'C':
            n = 4
        else:
            n = 5

        '''
            Create a function that return the list of days that exceed the limit of days
        '''
        overlapping_dates_in_all_ads = []
        for a in ads:
            if (duration_start - a.duration_start)>=timedelta(0) and (duration_end-a.duration_end)>=timedelta(0):
                # append from duration_start to a.duration_end
                for result in perdelta(duration_start,a.duration_end,timedelta(days=1)):
                    overlapping_dates_in_all_ads.append(result)

            elif (a.duration_start - duration_start)>timedelta(0) and (duration_end-a.duration_end)>=timedelta(0):
                for result in perdelta(a.duration_start,a.duration_end,timedelta(days=1)):
                    overlapping_dates_in_all_ads.append(result)

            elif (duration_start - a.duration_start)>=timedelta(0) and (duration_end-a.duration_end)<=timedelta(0):
                for result in perdelta(duration_start,duration_end,timedelta(days=1)):
                    overlapping_dates_in_all_ads.append(result)
            
            elif (a.duration_start - duration_start)>timedelta(0) and (duration_end-a.duration_end)<=timedelta(0):
                for result in perdelta(a.duration_start,duration_end,timedelta(days=1)):
                    overlapping_dates_in_all_ads.append(result)

        date_limit_exceed = list(set([x for x in overlapping_dates_in_all_ads if overlapping_dates_in_all_ads.count(x) > n]))

        if len(date_limit_exceed) > 0:
            raise forms.ValidationError( "ad limit conflict in the dates:" + str(date_limit_exceed))
        
        if duration_start >= duration_end:
            raise forms.ValidationError(
                "End Date must be after the Start date")

        if self.instance.id:
            return



        # Check if submitted dates overlaps with other dates:
        '''
            >>> from datetime import datetime, timezone
            >>> d = datetime.now(timezone.utc)
            >>> d
            datetime.datetime(2020, 3, 13, 6, 56, 27, 243397, tzinfo=datetime.timezone.utc)
            >>> a.duration_start - d
            datetime.timedelta(days=-5, seconds=39812, microseconds=756603)
        '''
        