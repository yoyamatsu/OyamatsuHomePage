#!/usr/bin/perl
use strict;
use warnings;
use Digest::SHA1;
use MIME::Base64;

print "Content-Type: text/html; charset=UTF-8\n\n";

my $username    = "admin";
my $password    = "2k26May30Fx4Wd";
my $output_path = "/home/ms001641/public_html/log/.htpasswd";

# SHA1形式でハッシュ生成
my $sha1   = Digest::SHA1->new;
$sha1->add($password);
my $hashed = "{SHA}" . encode_base64($sha1->digest, "");
my $line   = "$username:$hashed\n";

open(my $fh, '>', $output_path) or die "Cannot open: $!";
print $fh $line;
close($fh);

print "<p>生成完了：$output_path</p>";
print "<p>内容：$line</p>";
print "<p><b>このCGIは必ず削除してください！</b></p>";
