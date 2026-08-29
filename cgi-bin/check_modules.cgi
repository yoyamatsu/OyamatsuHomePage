#!/usr/bin/perl
use strict;
use warnings;

print "Content-Type: text/plain; charset=UTF-8\n\n";

# 各モジュールが使えるか確認
my @modules = ('Digest::SHA1', 'Digest::SHA', 'Digest::MD5', 'MIME::Base64');

for my $mod (@modules) {
    if (eval "use $mod; 1") {
        print "$mod : OK\n";
    } else {
        print "$mod : NG (使用不可)\n";
    }
}
