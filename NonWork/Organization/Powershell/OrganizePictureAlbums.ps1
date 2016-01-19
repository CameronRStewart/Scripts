[reflection.assembly]::LoadWithPartialName("System.Drawing")
$base_loc = 'D:\Bacchus\Pictures\Albums'
$test_pic = "$($base_loc)\Amsterdam\img_1264.jpg"
$pic = New-Object System.Drawing.Bitmap($test_pic)
$bitearr = $pic.GetPropertyItem(36867).Value
$string = [System.Text.Encoding]::ASCII.GetString($bitearr)
$formatted_date = [datetime]::ParseExact($string, "yyyy:MM:dd HH:mm:ss`0", $Null)

$year = $formatted_date.Year
$month = $formatted_date.Month
$day = $formatted_date.Day


<#

Run Function

For each directory:
    Get year and month for each file
    Create array each of years and months represented
If years array is of size 1:
    set year to that year
    If months array is of size 1:
        set month to that month
        e.g. 2012-October-Title
    Else:
        $seasons = whichSeasons(months)
        if $seasons is of size 1:
            write season
            e.g. 2012-Spring-Title
        else if $seasons is of size <= 2:
            season = season1/season2 (Spring/Summer)
            e.g. 2012-Spring/Summer-Title
        else:
            This will be a misc album of a particular year
            e.g. 2012-Misc-Title
            
            

Else
    This will be a misc album - named accordingly.
    e.g. Misc-Title
#>

<#
Which Season Function

Inputs:
    months (int array)   : array of months represented in album
Output:
    seasons (int arrray) : array with count of times each season is represented

seasons_of_year = int array containing count for fall, winter, spring, summer
        Fall = [September, October, November, December]
        Winter = [December, January, February, March]
        Spring = [March, April, May, June]
        Summer = [June, July, August, September]

Foreach month in months:
    foreach season in seasons_of_year:
        if month in season:
            season[month]++

#>

function whichSeasons
{
    param( [string[]]$months )
    # Need to numerize dates and seasons
    $seasons_of_year = @('Winter', 'Spring', 'Summer', 'Fall'), 
                            (
                                ('December', 'January', 'February'), 
                                ('March', 'April', 'May'), 
                                ('June', 'July', 'August'), 
                                ('September', 'October', 'November')
                            )


}