#!/usr/local/bin/perl

#===============================================================================
#	Access Log 蓄積プログラム
#
#		Create Date : 2002/11/04(Mon)
#		Author      : Yoshitaka Oyamatsu
#		Version     : 0.0
#===============================================================================

#-------------------------------------------------------------------------------
#	定数定義
#-------------------------------------------------------------------------------
$logdir   = '../html/log/';						#	データファイルディレクトリ
$logfile  = $logdir.'AccessLog.txt';			#	ログデータ

$usr_agnt = $ENV{'HTTP_USER_AGENT'};			#	ブラウザ情報
$referer  = $ENV{'HTTP_REFERER'};				#	リンク元URL
$rmt_host = $ENV{'REMOTE_HOST'};				#	リモートホスト情報
$rmt_addr = $ENV{'REMOTE_ADDR'};				#	IPアドレス情報
$rmt_user = $ENV{'REMOTE_USER'};				#	リモートユーザ情報
@days     = ('Sun' , 'Mon' , 'Tue' , 'Wed' , 'Thr' , 'Fri' , 'Sat');

#-------------------------------------------------------------------------------
#	メイン処理
#-------------------------------------------------------------------------------
$host_name = &get_host_name($rmt_addr);

($sec , $min , $hour , $mday , $mon , $year , $wday , $yday , $isdst) = localtime(time);

$hour   = sprintf("%02d" , $hour);
$min    = sprintf("%02d" , $min);
$sec    = sprintf("%02d" , $sec);
$year  += 1900;
$month  = sprintf("%02d" , $mon + 1);
$mday   = sprintf("%02d" , $mday);
$date   = "$year/$month/$mday $hour:$min:$sec $days[$wday]";

$log_data = "$date\t$usr_agnt\t$referer\t$rmt_host\t$host_name\t$rmt_user\n";

if(-e $logfile) {
	open(LOG , ">>$logfile");
}
else {
	open(LOG , ">$logfile");
}

print LOG $log_data;
close(LOG);

exit;

#-------------------------------------------------------------------------------
#	リモートホスト名取得処理
#-------------------------------------------------------------------------------
sub get_host_name {

	local($info_data) = @_;
	local($ip_addr , $visi_addr);

	if($info_data =~ /(\d+)\.(\d+)\.(\d+)\.(\d+)/) {
		$ip_addr   = "$1.$2.$3.$4";
		$visi_addr = gethostbyaddr(pack('C4' , $1 , $2 , $3 , $4) , 2);
		if($visi_addr ne '') {
			$rtn_addr = $visi_addr.'('.$ip_addr.')';
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
