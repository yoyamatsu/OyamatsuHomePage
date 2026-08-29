#!/usr/bin/perl

use strict;
use warnings;
use POSIX qw(strftime);
use Fcntl qw(:flock);       # 排他ロック定数の取込み

# character code : UTF-8

################################################################################
# Access Log
# Copyright(C) 2026 Yoshitaka Oyamatsu All rights reserved.
#
# Created : 2026/05/28(Th)
# Updated : 2026/06/06(Sa)
# Author  : Yoshitaka Oyamatsu
# Version : 0.1
################################################################################

# ログファイルのパス (書込み権限が必要)
my $log_file = "/home/ms001641/public_html/log/access_log.txt";
# エラーログファイルのパス (アクセスログがエラーになった時に出力)
my $error_log_file = "/home/ms001641/public_html/log/error_log.txt";

# 環境変数からアクセス情報を取得
my $rmt_addr  = $ENV{REMOTE_ADDR}     || "unknown";
my $referer   = $ENV{HTTP_REFERER}    || "-";
my $ua        = $ENV{HTTP_USER_AGENT} || "unknown";
my $host      = $ENV{HTTP_HOST}       || "unknown";
my $uri       = $ENV{REQUEST_URI}     || "/";
my $method    = $ENV{REQUEST_METHOD}  || "GET";

# ホスト名取得
my $host_name = get_host_name($rmt_addr);

# 日時 (日本時間)
my $datetime = strftime("%Y-%m-%d %H:%M:%S", localtime);

# ログに記録する1行
my $log_line = "$datetime\t$host_name\t$method\t$host$uri\t$referer\t$ua\n";

# ログファイルへ追記
if (open(my $fh, '>>', $log_file)) {
    flock($fh, LOCK_EX);                    # 排他ロック (同時アクセス対策)
    print $fh $log_line;
    flock($fh, LOCK_UN);                    # 排他ロック解除
    close($fh);
} else {
    my $err_msg = "$!";
    warn "Cannot open log: $err_msg";       # サーバーのerror_logにだけ記録

    # 独自エラーログに記録
    if (open(my $efh, '>>', $error_log_file)) {
        my $err_datetime = strftime("%Y-%m-%d %H:%M:%S", localtime);
        print $efh "$err_datetime\tCannot open access_log: $err_msg\n";
        close($efh);
    }
}

# HTTPレスポンス
print "Content-Type: text/html; charset=UTF-8\n\n";

#-------------------------------------------------------------------------------
# リモートホスト名取得処理
#-------------------------------------------------------------------------------
sub get_host_name {
    my($info_data) = @_;
    my($ip_addr, $visit_addr, $rtn_addr);

    if ($info_data =~ /(\d+)\.(\d+)\.(\d+)\.(\d+)/) {
        $ip_addr    = "$1.$2.$3.$4";
        $visit_addr = gethostbyaddr(pack('C4', $1, $2, $3, $4), 2);

        if (defined $visit_addr && $visit_addr ne '') {
            $rtn_addr = $visit_addr . '(' . $ip_addr . ')';
        } else {
            $rtn_addr = $ip_addr;
        }
    } else {
        $rtn_addr = $info_data // "unknown";
    }

    return $rtn_addr;
}
