#!/usr/bin/perl
use strict;
use warnings;
use POSIX qw(strftime);

# character code : UTF-8

################################################################################
# Access Log
# Copyright(C) 2026 Yoshitaka Oyamatsu All rights reserved.
#
# Created: 2026/05/28
################################################################################

# ログファイルのパス (書込み権限が必要)
my $log_file = "/home/ms001641/public_html/log/access_log.txt";

# 環境変数からアクセス情報を取得
my $ip      = $ENV{REMOTE_ADDR}     || "unknown";
my $referer = $ENV{HTTP_REFERER}    || "-";
my $ua      = $ENV{HTTP_USER_AGENT} || "unknown";
my $host    = $ENV{HTTP_HOST}       || "unknown";
my $uri     = $ENV{REQUEST_URI}     || "/";
my $method  = $ENV{REQUEST_METHOD}  || "GET";

# 日時 (日本時間)
my $datetime = strftime("%Y-%m-%d %H:%M:%S", localtime);

# ログに記録する1行
my $log_line = "$datetime\t$ip\t$method\t$host$uri\t$referer\t$ua\n";

# ログファイルへ追記
open(my $fh, '>>', $log_file) or die "Cannot open log: $!";
flock($fh, 2);          # 排他ロック (同時アクセス対策)
print $fh $log_line;
flock($fh, 8);          # 排他ロック解除
close($fh);

# HTTPレスポンス
print "Content-Type: text/html; charset=UTF-8\n\n";
