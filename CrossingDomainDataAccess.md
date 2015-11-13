# Introduction #

For static web page that wants to do mesh up under local file system, You can use the http://27.54.84.194/core/data/getservices/ to get all the services that was recorded in this project.


# Details #

The setting of the reply http header is like the following:

'Access-Control-Allow-Origin' = '**'
'Access-Control-Allow-Methods' = 'GET'
'Access-Control-Allow-Headers'] = 'X-Requested-With'**

So to successfully get the data, you should better use a xmlrequest with '
'Get'.

# Result XML #
An example of the result xml will looks like the following
```
<SERVICES>
<SERVICE name="Test1" type="FastFood" phone="12345" email="test1@hotmail.com" grade="1" privilege="normal" icon="icon" activity="0">
<latlong>-33917768,151102933</latlong>
<address>Fletcher St, Campsie, NSW 2194</address>
<description>Testing one.</description>
<days>Mon,Sat</days>
<age/>
</SERVICE>
<SERVICE name="test2" type="Cafe" phone="23456" email="test2@hotmail.com" grade="1" privilege="normal" icon="icon" activity="0">
<latlong>-33869628,151206954</latlong>
<address>Sydney, Australia</address>
<description>test description</description>
<days>Thu,Sat</days>
<age/>
</SERVICE>
<SERVICE name="test3" type="FastFood" phone="34556" email="test3@hotmail.com" grade="1" privilege="normal" icon="icon" activity="0">
<latlong>-33919219,151093154</latlong>
<address>Belmore, Australia</address>
<description>test3 desc</description>
<days>Wed,Sat</days>
<age/>
</SERVICE>
<SERVICE name="test4" type="FastFood" phone="312415" email="test4@hotmail.com" grade="1" privilege="normal" icon="icon" activity="0">
<latlong>-33951808,151138092</latlong>
<address>Rockdale, Australia</address>
<description>test 4 desc</description>
<days>Wed,Fri</days>
<age/>
</SERVICE>
<REPORT name="JOmY" who="SYSTEM" type="Breakfast">
<latlong>-33945171,151196762</latlong>
<address>Botany%2C%20Australia</address>
</REPORT>
<REPORT name="ThaiTime" who="SYSTEM" type="Lunch">
<latlong>-33869628,151206954</latlong>
<address>Sydney%2C%20Australia</address>
</REPORT>
<REPORT name="ThaiTime" who="SYSTEM" type="Breakfast">
<latlong>-33923400,151227462</latlong>
<address>Kingsford%2C%20Australia</address>
</REPORT>
</SERVICES>
```