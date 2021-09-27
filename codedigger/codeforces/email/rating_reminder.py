def get_rating_reminder_string():
    return """<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <meta name="viewport" content="width=device-width; initial-scale=1.0; maximum-scale=1.0;" />
    <!--[if !mso]--><!-- -->
    <link href='https://fonts.googleapis.com/css?family=Work+Sans:300,400,500,600,700' rel="stylesheet">
    <link href='https://fonts.googleapis.com/css?family=Quicksand:300,400,700' rel="stylesheet">
    <!-- <![endif]-->

    <title>Rating Change Reminder</title>

    <style type="text/css">
    	/* Codeforces Rank Related*/
		.rated-user {
    		font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
    		text-decoration: none;
    		font-weight: bold;
    		display: inline-block;
		}
		.user-black {
		    color: black !important;
		}
		.user-legendary {
		    color: red !important;
		}
		.legendary-user-first-letter {
		    color: black !important;
		}
		.user-red {
		    color: red !important;
		}
		.user-violet {
		    color: #a0a !important;
		}
		.user-orange {
		    color: #FF8C00 !important;
		}
		.user-blue {
		    color: blue !important;
		}
		.user-cyan {
		    color: #03A89E !important;
		}
		.user-green {
		    color: green !important;
		}
		.user-gray {
		    color: gray !important;
		}

        body {
            width: 100%;
            background-color: #ffffff;
            margin: 0;
            padding: 0;
            -webkit-font-smoothing: antialiased;
            mso-margin-top-alt: 0px;
            mso-margin-bottom-alt: 0px;
            mso-padding-alt: 0px 0px 0px 0px;
        }

        p,
        h1,
        h2,
        h3,
        h4 {
            margin-top: 0;
            margin-bottom: 0;
            padding-top: 0;
            padding-bottom: 0;
        }

        span.preheader {
            display: none;
            font-size: 1px;
        }

        html {
            width: 100%;
        }

        table {
            font-size: 14px;
            border: 0;
        }

        #rank-card{
            border: 1px solid gray;
            border-radius: 10px;
            border-left: 5px solid #747474;
        }
        #rating-change{
            border: 1px solid gray;
            border-radius: 10px;
            border-right: 5px solid #747474;
        }

        /* ----------- responsivity ----------- */

        @media only screen and (max-width: 640px) {
            /*------ top header ------ */
            .main-header {
                font-size: 20px !important;
            }
            .main-section-header {
                font-size: 28px !important;
            }
            .show {
                display: block !important;
            }
            .hide {
                display: none !important;
            }
            .align-center {
                text-align: center !important;
            }
            .no-bg {
                background: none !important;
            }
            /*----- main image -------*/
            .main-image img {
                width: 440px !important;
                height: auto !important;
            }
            /* ====== divider ====== */
            .divider img {
                width: 440px !important;
            }
            /*-------- container --------*/
            .container590 {
                width: 440px !important;
            }
            .container580 {
                width: 400px !important;
            }
            .main-button {
                width: 220px !important;
            }
            /*-------- secions ----------*/
            .section-img img {
                width: 320px !important;
                height: auto !important;
            }
            .team-img img {
                width: 100% !important;
                height: auto !important;
            }
        }

        @media only screen and (max-width: 479px) {
            /*------ top header ------ */
            .main-header {
                font-size: 18px !important;
            }
            .main-section-header {
                font-size: 26px !important;
            }
            /* ====== divider ====== */
            .divider img {
                width: 280px !important;
            }
            /*-------- container --------*/
            .container590 {
                width: 280px !important;
            }
            .container590 {
                width: 280px !important;
            }
            .container580 {
                width: 260px !important;
            }
            /*-------- secions ----------*/
            .section-img img {
                width: 280px !important;
                height: auto !important;
            }
        }
    </style>
</head>


<body class="respond" leftmargin="0" topmargin="0" marginwidth="0" marginheight="0">
    <!-- pre-header -->
    <table style="display:none!important;">
        <tr>
            <td>
                <div style="overflow:hidden;display:none;font-size:1px;color:#ffffff;line-height:1px;font-family:Arial;maxheight:0px;max-width:0px;opacity:0;">
                    Codeforces Rating Update Mail
                </div>
            </td>
        </tr>
    </table>
    <!-- pre-header end -->
    <!-- header -->
    <table border="0" width="100%" cellpadding="0" cellspacing="0" bgcolor="ffffff">
        <tr>
            <td align="center">
                <table border="0" align="center" width="590" cellpadding="0" cellspacing="0" class="container590">
                    <tr>
                       <td height="15" style="font-size: 15px; line-height: 15px;">&nbsp;</td>
                    </tr>
                    <tr>
                        <td align="center">
                            <table border="0" align="center" width="590" cellpadding="0" cellspacing="0" class="container590">
                                <tr>
                                    <td align="center" style="height:70%;">
                                        <a href="http://codedigger.tech/" style="display: block; border-style: none !important; border: 0 !important;"><img width="50%" border="0" src="https://lh3.googleusercontent.com/oYrlqJcNfzGmCl84iQe48NmDnTWer3CIWudMmiDeuY702E5nUkHsC2YAbutwOj53JM0Ik9koxaIobegGoO5z0fB7GjKjyQEccrBoZCQozA4oOUYlCMXrvMN--Xwkxz-_c4k55lUo5kK4aF-UybRXGcgu3UejkK9_F8yQ3W2FRyrjmqHyIaaKLGJsAgRTxZWyI2OD8gK-s76ebvbQQcQeoQf3lc_FAuTLTqjxDluz3WHWbPpDKtQ8Z8lmZFxzRH1WpXFjGW5XW1WC-cIdBpf9C30Scjzi6DjrzOM84GtatdhgIc5jeH_sXt5VKHalxYR2Zt4DvKb1c3xQS1f6uceEkeUlTNcH2_X-8jRFAtPitSCYdgYCMjsKAg_wYta53qUpXa6dJ1hDdzY-3wCm6vorGejyHZJK3v48XLG00EIbJ7wkyGQfK41klxbB4dROPEshvHAE3XDpon34Av1DAtFATW6ZwYkTWh0-3l2AfPEo__pXwyB9PEQg7KaEGwDzrtkiFboyRn19_GK2jG5FEtR-lI2CToUO9n95gsCjyq_cw2UPLkNI10GxNk8EGcJk83E4XfKIktMStxcr7C-k4PhzvEm-7GTxhzuQDTnO8jJCXoUHZSkxB50O_hGYcZ4SiKgtWL0P1ByZkOuFCNtnDjvB2IdnLBNmxPM13ol0qKE0vMH9gCci9S7U4tXX0vuHYA=w1366-h376" alt="Codedigger LOGO" />
                                        </a>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    <tr>
                        <td height="15" style="font-size: 15px; line-height: 15px;">&nbsp;</td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
    <!-- end header -->
    <!-- big image section -->
    <table border="0" width="100%" cellpadding="0" cellspacing="0" bgcolor="ffffff" class="bg_color">

        <tr>
            <td align="center" style="background-color: #ffffff !important">
                <table border="0" align="center" width="590" cellpadding="0" cellspacing="0" class="container590">
                    <tr>
                        <td height="15" style="font-size: 15px; line-height: 15px;">&nbsp;</td>
                    </tr>
                    <tr>
                        <td align="center" style="color: #343434; font-size: 24px; font-family: Quicksand, Calibri, sans-serif; font-weight:700;letter-spacing: 3px; line-height: 35px;" class="main-header">
                            <div style="line-height: 35px" >

                                HI CODER! <a href="https://codeforces.com/profile/{{rating_change.handle}}">{% if rating_change.isnewlegendary %}
                                <span class="legendary-user-first-letter rated-user">{{rating_change.handle.0}}</span><span class="{{rating_change.newcolor}} rated-user">{{rating_change.handle|slice:"1:"}}</span>{% else %}<span class="{{rating_change.newcolor}} rated-user">{{rating_change.handle}}</span>{% endif %}</a>,

                            </div>
                        </td>
                    </tr>
                    <tr>
                        <td height="20" style="font-size: 20px; line-height: 20px;">&nbsp;</td>
                    </tr>
                    <tr>
                        <td align="center">
                            <table border="0" width="40" align="center" cellpadding="0" cellspacing="0" bgcolor="eeeeee">
                                <tr>
                                    <td height="2" style="font-size: 2px; line-height: 2px;">&nbsp;</td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    <tr>
                        <td height="20" style="font-size: 20px; line-height: 20px;">&nbsp;</td>
                    </tr>
                    <tr>
                        <td align="center">
                            <table border="0" width="400" align="center" cellpadding="0" cellspacing="0" class="container590">
                                <tr>
                                    <td align="center" style="color: #888888; font-size: 16px; font-family: 'Work Sans', Calibri, sans-serif; line-height: 24px;">
                                        <div id="rating-change" style="line-height: 24px">
											The Rating Change of
                                            <br> <a href="https://codeforces.com/contest/{{rating_change.contestId}}/ratings/friends/true">{{rating_change.contestName}}</a>
                                            <br>
                                            are out now...

											<br>

											{% if rating_change.newRank != rating_change.oldRank and rating_change.newRating > rating_change.oldRating  %}
												Congratulations on becoming
                                            <br>
											{% if rating_change.isnewlegendary %}
											<span class="legendary-user-first-letter rated-user">{{rating_change.newRank.0}}</span><span class="{{rating_change.newcolor}} rated-user">{{rating_change.newRank|slice:"1:"}}</span>
											{% else %}
											<span class="{{rating_change.newcolor}} rated-user">{{rating_change.newRank}}</span>
											{% endif %}
											{% endif %}
                                            <br>

                                        </div>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    <tr>
                        <td height="15" style="font-size: 15px; line-height: 15px;">&nbsp;</td>
                    </tr>
                    <tr>
                        <td align="center">
                            <table border="0" width="400" align="center" cellpadding="0" cellspacing="0" class="container590">
                                <tr>
                                    <td align="center" style="color: #888888; font-size: 16px; font-family: 'Work Sans', Calibri, sans-serif; line-height: 24px;">
                                        <div style="line-height: 24px">

                                        <span id = 'old-rank' style="display: inline-block;width: 90px;height: 60px;">
                                            {% if rating_change.isoldlegendary %}
                                            <span class="{{rating_change.oldcolor}} rated-user">{{rating_change.oldRating}}</span>
                                            <br>
                                            <span class="legendary-user-first-letter rated-user" style="display: inline;">{{rating_change.oldRank.0}}</span><span class="{{rating_change.oldcolor}} rated-user" style="display: inline;">{{rating_change.oldRank|slice:"1:"}}</span>

                                            {% elif rating_change.oldrating == 0 %}
                                            <span class="user-black">{{rating_change.oldRating}} <br>Unrated</span>
                                            {% else %}
                                            <span class="{{rating_change.oldcolor}} rated-user">{{rating_change.oldRating}} <br> {{rating_change.oldRank}}</span>

                                            {% endif %}
                                        </span>
                                        <span id = "arrow" style="display: inline-block;width: 80px;height:60px">
                                            <img width="100%" height="70%" border="0" src="https://lh3.googleusercontent.com/WTiHNG2tfrdXKkpIf_qyjSF7kfzVGKGAUZVBX6S1ZrtQKocKnN6jn66IOwSvAoeehBmpjwVdlz2RdZoAcZqEwCR9cKaoMng3V10DstLbQVZ9Kb4RN6qmHGdx3K516bGnmX5kgz9VVoRFgERk3aEEkyivHz80tilxtEVePWEMkPY5ZhXruwmrZiZ8zDkkcgzuqN7nYpfjZQ4a061YHnW-6RxCOnZD84daoRn90nDowCgSE2hyRB49t1tt3uWRbgQwlCi0iO_lKrdJpRbNfSlrKdKT-_wuwb5d7uv8CAdXCKaK3BC7hQRfq28q7hJOozv3qohM1gb4byTMCtUJN7pMf2Fcts3i9mzzqoCdgpW_tOHm59n5oR60Ckn3gwaOIjCeEqD1Wge0Pkz79CU_j-ey67HbrEUpQCwDiCOLR3gf6Un1dYVMBgB0QjePwdJLa8N5D7WmIj3pOjQcRo2ljhRjNZ8bgMgI1o2osKhyl4r34VzdM6vRYWC1bU16iVDNySG4pLbMTDmbt77BxSKv2BFqwbaO884JMLYVsojSKZfncZk8FzDJRDMxlXJJCMVEJgcZBGwRpeVq0kyJ2UTZ3Uslqlaxp8cZk0tH-REeUwqzoke3nap4tAA8p3hZfDkWH33giqVTxYJPD0t0lmH5_Wt8BMOBjvetxfnkXKwYYDdmzTrO77_fDAw0rYuR_sysWA=w378-h170" alt="To" />
                                        </span>
                                        <span id = "new-rating" style="display: inline-block;width: 90px;height: 60px;">
                                            {% if rating_change.isnewlegendary %}
                                            <span class="{{rating_change.newcolor}} rated-user">{{rating_change.newRating}}</span>
                                            <br>
                                            <span class="legendary-user-first-letter rated-user"style="display: inline;">{{rating_change.newRank.0}}</span><span class="{{rating_change.newcolor}} rated-user"style="display: inline;">{{rating_change.newRank|slice:"1:"}}</span>

                                            {% else %}
                                            <span class="{{rating_change.newcolor}} rated-user">{{rating_change.newRating}} <br>{{rating_change.newRank}}</span>
                                            {% endif %}

                                        </span>

                                        </div>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    <tr>
                        <td height="15" style="font-size: 15px; line-height: 15px;">&nbsp;</td>
                    </tr>
                    <tr>
                        <td align="center">
                            <table border="0" width="400" align="center" cellpadding="0" cellspacing="0" class="container590">
                                <tr>
                                    <td align="center" style="color: #888888; font-size: 16px; font-family: 'Work Sans', Calibri, sans-serif; line-height: 24px;">
                                        <div id="rank-card" style="line-height: 24px">

                                            {% if cdata %}
                                            <h4>Rank -</h4>
                                                World Rank - {{cdata.worldRank}} / {{cdata.contest.participants}}
                                            <br>
                                                Country Rank  - {{cdata.countryRank}} / {{cdata.totalCountryParticipants}}
                                            <br>
                                                Organization Rank - {{cdata.organizationRank}} / {{cdata.totalOrganizationParticipants}}
                                            <br>
                                            {% endif %}
                                            <!--Sharable Link

                                            Created by Codedigger

                                            // Information about codedigger -->
                                        </div>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
    <!-- end section -->
    <!-- contact section -->
    <table border="0" width="100%" cellpadding="0" cellspacing="0" bgcolor="ffffff" class="bg_color">
        <tr class="hide">
            <td height="25" style="font-size: 25px; line-height: 25px;">&nbsp;</td>
        </tr>
        <tr>
            <td height="25" style="font-size: 25px; line-height: 25px;">&nbsp;</td>
        </tr>
        <tr>
            <td height="20" style="border-top: 2px solid #e0e0e0;font-size: 20px; line-height: 20px;">&nbsp;</td>
        </tr>
        <tr>
            <td align="center">
                <table border="0" align="center" width="590" cellpadding="0" cellspacing="0" class="container590 bg_color">
                    <tr>
                        <td>
                            <table border="0" width="300" align="left" cellpadding="0" cellspacing="0" style="border-collapse:collapse; mso-table-lspace:0pt; mso-table-rspace:0pt;" class="container590">
                                <tr>
                                    <!-- logo -->
                                    <!--<td align="left">
                                        <a href="" style="display: block; border-style: none !important; border: 0 !important;"><img width="50%" border="0" src="https://lh3.googleusercontent.com/cz1cLquiLjSoxORU1jZHNWyIB2_GrsMFkLFSHd0oTj71fTg4MRazGTyAgAPz7R9qtZdXMxmzPPi8cIrHkC_9p6wDh8ACMPgddpmWNKmBroxOVLg6BxpV1utyu5QGLsb1khwgIqADmdw8vFVFLYv2GBJbxrH0c1HQCY_6ekCavDpnUULtUUW936CJ_-b1OtKri0Z51pC-VU1ns8FD9YXM2bsxZfipy3txFWacOAkLKYr9yMb2jiGoxDonpXVLsvsDxnr5VcIpL72SFR3ZgeB1LfjWp50eloo7CFXFiCvDMIPS0QnrTByN1r0JFBAM68SNeOAHrJRH_kLWvVqSZWyTvrXEn8pTo2nZUWM9SYPPG8r13HmdzJBwELcOfTSo5ytdm_f9JUbT0M-JDGhCfLZbXACa7kpGeENVzTIGop8KrtUAbuQS0K7sGwHb0phAIL_Z72YmTByGUwf_8OC01D8FYKnXNzwS5ub3tFOrLt0MHcALTaytC_Hm0ZC_TmVyJFUH08alJPRgAuosCWm0lr0bwAfy8klIGxl_P4kbLF1HH0uaftf45vDHFz8puujiXDP_2gAlh_Vi24v8hBmG5dYPYTHUNQPrcz1o-fwGmq9PwjkTb6iarfLokOr2buYrZVYuwG0jQVV_8S-GqNXsjS-gqxA23KnQLenpCxdk6LygOkbtHC1YZeT_gg97bqUZ_g=w1031-h284-no?authuser=0" alt="" /></a>
                                    </td>-->
                                </tr>
                                <tr>
                                    <td align="left" style="color: #888888; font-size: 14px; font-family: 'Work Sans', Calibri, sans-serif; line-height: 23px;" class="text_color">
                                        <div style="color: #333333; font-size: 14px; font-family: 'Work Sans', Calibri, sans-serif; font-weight: 600; mso-line-height-rule: exactly; line-height: 23px;">
                                            Email us: <br/> <a href="mailto:codedigger1.0@gmail.com" style="color: #888888; font-size: 14px; font-family: 'Hind Siliguri', Calibri, Sans-serif; font-weight: 400;"> codedigger1.0@gmail.com </a>
                                        </div>
                                    </td>
                                </tr>
                            </table>
                            <table border="0" width="200" align="right" cellpadding="0" cellspacing="0" style="border-collapse:collapse; mso-table-lspace:0pt; mso-table-rspace:0pt;" class="container590">
                                <tr>
                                    <td>
                                        <table border="0" align="right" cellpadding="0" cellspacing="0">
                                            <tr>
                                                <td>
                                                    <a href="#" style="display: block; border-style: none !important; border: 0 !important;"><img width="24" border="0" style="display: block;" src="http://i.imgur.com/Qc3zTxn.png" alt=""></a>
                                                </td>
                                                <td>&nbsp;&nbsp;&nbsp;&nbsp;</td>
                                                <td>
                                                    <a href="#" style="display: block; border-style: none !important; border: 0 !important;"><img width="24" border="0" style="display: block;" src="http://i.imgur.com/RBRORq1.png" alt=""></a>
                                                </td>
                                                <td>&nbsp;&nbsp;&nbsp;&nbsp;</td>
                                                <td>
                                                    <a href="#" style="display: block; border-style: none !important; border: 0 !important;"><img width="24" border="0" style="display: block;" src="http://i.imgur.com/Wji3af6.png" alt=""></a>
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
        <tr>
            <td height="20" style="font-size: 20px; line-height: 20px;">&nbsp;</td>
        </tr>
    </table>
    <!-- end section -->
</body>
</html>"""
