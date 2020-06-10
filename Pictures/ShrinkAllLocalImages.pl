#!/usr/local/bin/perl
#
# Make simple beveled button with some text on it and output to STDOUT in GIF format
#
# a little more complex - the gradient colours are passed in as CGI parameters, and the text and text colour are specified
#
# to embed this image in a web page, use:
# img src="imagedemo3.pl?colour1=ff0000&colour2=0000ff&text=My%20First%20Button"

use Image::Magick;

my @PictureArray = `dir . /b /o:e`;

my $count = 0;
foreach $Picture (@PictureArray) 
	{
		$Picture =~ s/\n//;
		if( ($Picture =~ m/\.jpg/ || $Picture =~ m/\.jpe/ || $Picture =~ m/\.jpeg/ || $Picture =~ m/\.gif/) 
			&& $Picture !~ m/\.bak/ 
			&& $Picture !~ m/^60x60/ 
			&& $Picture !~ m/^180x180/ )
		{
			# Create 60x60 thumbnail of current image...
			my($image, $x);
			$image = Image::Magick->new;
			$x = $image->Read($Picture);
			warn "$x" if "$x";
			$x = $image->Scale(geometry=>'60x60');
			warn "$x" if "$x"; 			
			$x = $image->Write('60x60_' . $Picture);
			warn "$x" if "$x";
			undef($image);

			# Create 180x180 thumbnail of current image...
			my($image, $x);
			$image = Image::Magick->new;
			$x = $image->Read($Picture);
			warn "$x" if "$x";
			$x = $image->Scale(geometry=>'180x180');
			warn "$x" if "$x"; 			
			$x = $image->Write('180x180_' . $Picture);
			warn "$x" if "$x";
			undef($image);

			print "($Picture)\n";
			$count++;
		}
	}
print "Total pictures thumbnailed = ($count)\n";

exit (0);
