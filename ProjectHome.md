Wave robot for automatically converting certain units:

  * R$2.00 (USD$ ?)
  * 10cm (?")
  * 10km (? miles)
  * 100kph (?mph)
  * 100L (? gallons)

The inspiration was my blog.

I live now in Brazil, but know that some of my readers are North Americans and might not know the metric system very well or how much a Brazilian Real is worth.
A one time I made javascript function to convert these things automatically. Here I've done the same thing with Python and a wave robot.

The code looks can handle postfix and prefix units (but not both).
It searches for certain combinations and won't see other combinations (i.e. it won't try to convert cm to mph for example).

The code also tries to give the equivalent number of significant digits (unless the error is greater than 10%). For example 10 inches converts to 25cm (and not 25.4 cm which is more exact).  However 1 inch converts to 2.5cm and not 3cm since the error is too great.

The format is something like:

`<number> <unit1> (? <unit2>)`

or

`<unit1> <number> (<unit2> ?)`

Here are the regular expressions that are recognized:

**Real** `<->` **USD**<br>
'R\s?\$|BRL\s?\$' to \$|USD\s?\$'<br>
<br>
<b>cm</b> <code>&lt;-&gt;</code> <b>inches</b><br>
'cm|centimeters?' to '"|inch(?:es)?'<br>
<br>
<b>km</b> <code>&lt;-&gt;</code> <b>miles</b><br>
'<a href='Kk.md'>Kk</a>m' to 'miles?'<br>
<br>
<b>kph</b> <code>&lt;-&gt;</code> <b>mph</b><br>
'<a href='Kk.md'>Kk</a>m/h|kph' to '<a href='Mm.md'>Mm</a>ph|miles? per hour'<br>
<br>
<b>Celsius</b> <code>&lt;-&gt;</code> <b>Fahrenheit</b><br>
'<a href='Cc.md'>Cc</a>|<a href='C.md'>C</a>elsius|°C' to '<a href='Ff.md'>Ff</a>|<a href='Ff.md'>Ff</a>ahrenheit|°F'<br>
<br>
<b>kg</b> <code>&lt;-&gt;</code> <b>lbs</b><br>
'<a href='Kk.md'>Kk</a>g|kilograms?' to 'lbs?|lbs?\.|pounds?<br>
<br>
<b>Liters</b> <code>&lt;-&gt;</code> <b>US Gallons</b><br>
'<a href='Ll.md'>Ll</a>|litres?|liters?' to 'gals?|gallons?|gals?\.'<br>
