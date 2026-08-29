#!/usr/bin/perl
use strict;
use warnings;

# character code : UTF-8

################################################################################
# Access Counter
# Copyright(C) 2026 Yoshitaka Oyamatsu All rights reserved.
#
# Created: 2026/05/28
################################################################################

# カウントファイルのパス（サーバーの絶対パスに合わせて変更）
my $count_file = '/home/ms001641/public_html/data/counter/count.txt';

# digit画像のURLパス
my $digit_dir = '/images/ping/counter/digits';

# digit画像の拡張子
my $digit_ext = 'png';

# 表示する最小桁数（足りない場合は先頭を0埋め）
my $digit_min = 6;

# ---- カウントアップ ----
open(my $fh, '+<', $count_file) or die "Cannot open $count_file: $!";
flock($fh, 2);  # 排他ロック
my $count = <$fh> // 0;
chomp $count;
$count++;
seek($fh, 0, 0);
truncate($fh, 0);
print $fh $count;
flock($fh, 8);  # ロック解除
close($fh);

# ---- digit画像HTMLを生成して出力 ----
my $padded = sprintf("%0${digit_min}d", $count);

print "Content-type: text/html\n\n";

for my $d (split //, $padded) {
    print qq(<img src="$digit_dir/$d.$digit_ext" alt="$d" style="vertical-align: middle;">);
}
