#!/usr/bin/perl
print "Content-Type: text/plain\n\n";
print "Perl OK\n";

require MIME::Base64;
print "MIME::Base64: OK\n";

require Digest::SHA1;
print "Digest::SHA1: OK\n";

require Digest::SHA;
print "Digest::SHA: OK\n";

require Digest::MD5;
print "Digest::MD5: OK\n";
