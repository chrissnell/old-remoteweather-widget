#!/usr/bin/perl

use Device::WxM2;
use RRDs;
use Redis;


my $ws = new Device::WxM2 ("/dev/tty.usbserial");

my $time_to_die = 0;

until ($time_to_die) {

    my $r = Redis->new( server => '127.0.0.1:6379',
                        reconnect => 60 );

    my $itemp = $ws->getInsideTemp; 
    my $otemp = $ws->getOutsideTemp; 
    my $wspeed = $ws->getWindSpeed; 
    my $wdir = $ws->getWindDir; 
    my $ihumidity = $ws->getInsideHumidity;
    my $ohumidity = $ws->getOutsideHumidity; 
    my $pressure = $ws->getBarometricPressure;
    my $rainfall = $ws->getDailyRain;

    $r->mset( lastobs   => time,
              itemp     => $itemp,
              otemp     => $otemp,
              wspeed    => $wspeed,
              wdir      => $wdir, 
              pressure  => $pressure,
              ihumidity => $ihumidity,
              ohumidity => $ohumidity,
              rainfall  => $rainfall ); 

    $r->save;

    print "Inside temperature: $itemp\n";
    print "Outside temperature: $otemp\n";

    print "Inside humidity: $ihumidity\n";
    print "Outside humidity: $ohumidity\n";
    print "Barometric pressure: $pressure\n";

    print "Wind Speed: $wspeed\n";
    print "Wind Direction: $wdir\n";

    print "Today's rainfall: $rainfall\n";

    print "\n------------------------------------------------\n\n";

    my $rrd = "broadmoor.rrd";

    my $update = "N" . ":" . "$itemp" . ":" . $otemp . ":" . $wspeed . ":" . $wdir;

    RRDs::update($rrd, $update);

    sleep(10);
}

sub signal_handler {
    $time_to_die = 1;
}  

$SIG{INT} = $SIG{TERM} = $SIG{HUP} = \&signal_handler; 
