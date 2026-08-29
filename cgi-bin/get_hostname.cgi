#!/usr/bin/perl

use strict;
use warnings;
use POSIX qw(strftime);

my $rmt_addr  = $ENV{REMOTE_ADDR};               # IPアドレス情報
my $host_name = get_host_name($rmt_addr);

# HTTPレスポンス
#print "Content-Type: text/html; charset=UTF-8\n\n";
print "IPアドレス情報: $rmt_addr<br>\n";
print "ホスト名　　　: $host_name<br>\n";

#-------------------------------------------------------------------------------
# リモートホスト名取得処理
#-------------------------------------------------------------------------------
sub get_host_name {
    my($info_data) = @_;
    my($ip_addr, $visit_addr, $rtn_addr);

    if($info_data =~ /(\d+)\.(\d+)\.(\d+)\.(\d+)/) {
        $ip_addr    = "$1.$2.$3.$4";
        $visit_addr = gethostbyaddr(pack('C4', $1, $2, $3, $4), 2);

        if(defined $visit_addr && $visit_addr ne '') {
            $rtn_addr = $visit_addr . '(' . $ip_addr . ')';
        }
        else {
            $rtn_addr = $ip_addr;
        }
    }
    else {
        $rtn_addr = $info_data;
    }

    return $rtn_addr;
}
