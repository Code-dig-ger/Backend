def get_rating_reminder_string():
    return """
<!DOCTYPE html>
<html>
  <head>
    <title>Rating Change remainder</title>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <link
      href="https://fonts.googleapis.com/css?family=Work+Sans:300,400,500,600,700"
      rel="stylesheet"
    />
    <link
      href="https://fonts.googleapis.com/css?family=Quicksand:300,400,500,600,700"
      rel="stylesheet"
    />
    <style type="text/css">
      @media screen {
        @font-face {
          font-family: "Lato";
          font-style: normal;
          font-weight: 400;
          src: local("Lato Regular"), local("Lato-Regular"),
            url(https://fonts.gstatic.com/s/lato/v11/qIIYRU-oROkIk8vfvxw6QvesZW2xOQ-xsNqO47m55DA.woff)
              format("woff");
        }

        @font-face {
          font-family: "Lato";
          font-style: normal;
          font-weight: 700;
          src: local("Lato Bold"), local("Lato-Bold"),
            url(https://fonts.gstatic.com/s/lato/v11/qdgUG4U09HnJwhYI-uK18wLUuEpTyoUstqEm5AMlJo4.woff)
              format("woff");
        }

        @font-face {
          font-family: "Lato";
          font-style: italic;
          font-weight: 400;
          src: local("Lato Italic"), local("Lato-Italic"),
            url(https://fonts.gstatic.com/s/lato/v11/RYyZNoeFgb0l7W3Vu1aSWOvvDin1pK8aKteLpeZ5c0A.woff)
              format("woff");
        }

        @font-face {
          font-family: "Lato";
          font-style: italic;
          font-weight: 700;
          src: local("Lato Bold Italic"), local("Lato-BoldItalic"),
            url(https://fonts.gstatic.com/s/lato/v11/HkF_qI1x_noxlxhrhMQYELO3LdcAZYWl9Si6vvxL-qU.woff)
              format("woff");
        }
      }

      /* CLIENT-SPECIFIC STYLES */
      body,
      table,
      td,
      a {
        -webkit-text-size-adjust: 100%;
        -ms-text-size-adjust: 100%;
      }

      img {
        -ms-interpolation-mode: bicubic;
      }

      /* RESET STYLES */
      img {
        border: 0;
        height: auto;
        line-height: 100%;
        outline: none;
        text-decoration: none;
      }

      table {
        border-collapse: collapse !important;
      }

      h1,
      h2,
      h3,
      h4,
      h5,
      h6 {
        font-family: Quicksand, Calibri, sans-serif;
        font-weight: 700;
      }

      body {
        height: 100% !important;
        margin: 0 !important;
        padding: 0 !important;
        width: 100% !important;
      }

      /* iOS BLUE LINKS */
      a[x-apple-data-detectors] {
        color: inherit !important;
        text-decoration: none !important;
        font-size: inherit !important;
        font-family: inherit !important;
        font-weight: inherit !important;
        line-height: inherit !important;
      }

      /* MOBILE STYLES */
      @media screen and (max-width: 600px) {
        h1 {
          font-size: 32px !important;
          line-height: 32px !important;
        }
      }
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

      /* ANDROID CENTER FIX */
      div[style*="margin: 16px 0;"] {
        margin: 0 !important;
      }
    </style>
  </head>

  <body
    style="
      background-color: #f4f4f4;
      margin: 0 !important;
      padding: 0 !important;
    "
  >
    <!-- HIDDEN PREHEADER TEXT -->
    <div
      style="
        display: none;
        font-size: 1px;
        color: #fefefe;
        line-height: 1px;
        font-family: 'Lato', Helvetica, Arial, sans-serif;
        max-height: 0px;
        max-width: 0px;
        opacity: 0;
        overflow: hidden;
      "
    >
      We're thrilled to announce that your Codeforces rating has changed.
    </div>
    <table border="0" cellpadding="0" cellspacing="0" width="100%">
      <!-- LOGO -->
      <tr>
        <td bgcolor="#FFA73B" align="center">
          <table
            border="0"
            cellpadding="0"
            cellspacing="0"
            width="100%"
            style="max-width: 600px"
          >
            <tr>
              <td
                align="center"
                valign="top"
                style="padding: 20px 10px 20px 10px"
              ></td>
            </tr>
          </table>
        </td>
      </tr>
      <tr>
        <td bgcolor="#FFA73B" align="center" style="padding: 0px 10px 0px 10px">
          <table
            border="0"
            cellpadding="0"
            cellspacing="0"
            width="100%"
            style="max-width: 600px"
          >
            <tr>
              <td
                bgcolor="#ffffff"
                align="center"
                style="
                  padding: 30px 20px 2px 20px;
                  border-radius: 4px 4px 0px 0px;
                "
              >
                <a
                  href="https://codedigger.tech/"
                  style="
                    display: block;
                    border-style: none !important;
                    border: 0 !important;
                  "
                  ><img
                    width="50%"
                    style="min-width: 250px"
                    border="0"
                    src="https://lh3.googleusercontent.com/pw/ACtC-3fvyif39GMTNTsxXveZB0z3nPAxcaaYnTAw-bVROn58ZTkqO2k-kJngoftU8_xNPBdI5QB-gXgoQKOfBAndXRJiAxY6UxT96IlPf_wv_AihsFI_7dtmqchmJ9OfifaZcdH6JgPMxU2w1qUKGVbQBEf3=w290-h49-no?authuser=0"
                    alt="Codedigger"
                  />
                </a>
              </td>
            </tr>
            <tr>
              <td
                bgcolor="#ffffff"
                align="center"
                valign="top"
                style="
                  padding: 0px 20px 20px 20px;
                  border-radius: 0px;
                  color: #111111;
                  font-family: 'Lato', Helvetica, Arial, sans-serif;
                  letter-spacing: 1px;
                "
              >
                <h1
                  style="
                    font-size: 30px;
                    font-weight: 600;
                    margin: 2;
                    line-height: 48px;
                  "
                >
                  HI CODER!
                  <a
                    href="https://codeforces.com/profile/{{rating_change.handle}}"
                    style="text-decoration: none"
                    >
                    {% if not rating_change.isnewlegendary %}
                      <span class="rated-user {{rating_change.newcolor}}">
                        {{rating_change.handle}}
                      </span>
                    {% else %}
                      <span class="legendary-user-first-letter rated-user">
                        {{rating_change.handle.0}}
                      </span><span class="{{rating_change.newcolor}} rated-user">
                        {{rating_change.handle|slice:"1:"}}
                      </span>
                    {% endif %}
                  </a>
                </h1>
                <p
                  style="
                    color: #666666;
                    font-family: 'Lato', Helvetica, Arial, sans-serif;
                    font-size: 18px;
                    font-weight: 400;
                    line-height: 25px;
                  "
                >
                  The Rating Change of <br />
                  <a
                    href="https://codeforces.com/contest/{{rating_change.contestId}}/ratings/friends/true"
                    style="color: #ffa73b; text-transform: capitalize"
                    >{{rating_change.contestName}}</a
                  >
                  <br />are out now...
                </p>

                <img
                  src= 
                  {% if rating_change.newRating > rating_change.oldRating %}
                    "https://lh3.googleusercontent.com/VdT4Fh3WZE6T-nGBKZ4ZapsQ4xDmSnbVQb_61B8gpoOLHMTsd8lIUd0ghMpf3TFz-hPUFpdQrwWGB8Kyvb6R4g0j9kthWs-wps3Pxm4xkeYr6n5Wr459Rj9PcmH1ZOAVpeb24a8ISXK5leYbyiXi_KGkupLEbWCWZ76PT8mQYw3rByD2oK-9Ey-XZFs123V8ji_qJ6M7cXudLErb5CCFAie_aov_FdJk49kL-HtaGWaz4f8quxTpuZRBYhXbMLFSnelCppJrNh3snyaXezxCwdBvJrzQtN5Vy7C_1Bhue3YhcPtorA9US8IBO73xkNBq6_F-n3vWfSY_X0lDUZ_oY8W6nGF-Ng1KgA5YcsNQSwkQTTULKDJFhlfopxqNMbiXAstTKpn8SaD8RcqOw1iL2CQOMa_ZS82g1eGCeKSJYhM214Bca-LCfSYvMyO63IO--T47NmIHmt__Wa_a5XvANB82Gon63QzJg24cHaZRFlM6D3QOrt0lAoQyDsC00pcqIZAfIqnLj9QJVGdaRbU2o6dlZ40Usoq2DAKsExZliSc1yK7nYNlBu-XHcyvCxOYt_vnHWH_KU88pIXqBbed39NyHLrVfUK3SX0IpnC2iaRfrnKI2xOv-qnE3_0qtz2mita33qTZLGarDmrycZAmMxgtx2AGepOhjj9Af6DRQmvUWTfG39DrM2PoDjsjiQwAHTvdk99gJl5-jkvT-bVLSbk4=w1116-h637-no?authuser=0"
                  {% else %}
                    "https://lh3.googleusercontent.com/Zc1VgAKnfoJzcUgSMxBu0FrTSNg1L4KkwZftNKB3aDfxm9kK3C16DAmlgYgW6ejP_Nan0ResRzHj0s8rqvs0rOPNeN3LtJerYwv3-goG8BUp80e1Y9YyiX0HoJ-xpU-X2-TRFyJ6Jr5PMkagTm9FAMB5ZMqbMDNaiT4iEO1Sjh7-QDAPyUrKVNOfUWVXCFn1eadMtv8xzCsUV3cYHl2miLEOroTC4kum3HmoxUaZ_jWmu4kRXqbNPbcou75njTwH5SEIJuG2SpZ1K6ymxb3SHhsBVcYzaIP5VRWKX4zPxdS1TKU_5UMPZnJLvDS6H_cSYmmCzZHys9BWW7YPyvUbXiLEOoXkaa3JMIbRcuRldqKtgJdQARwTK9QeWfLCo-jv3ORx7PF6ZZ1E_0Xzmoxh3wzIPOrKGlNsuFlxrhbod6KvDaAXhefwxhDKDQzz7WPBxK1jCoFMGFfTlXh-X4L2cA45Jkjtokr3evZQUPLiRomzzY1bLtRFoG5I20bVUSS9i1QarSO5I7shzPeOrliy2d8B0axpmAhC9cozEQSmJAReQgHiVJAI1gBCwFsNGMiLLCm8DeSCHUERa7SNV56tcotTjPgU2P56qoAgKNYZPKRcno2voSYyTgPrmKL9uE8fmXzhlYJwo_g3SttXlLYlKIgdYb-VAmUEM-LHUGzuMOlIKliCMCD7hiTz74vOWyBMGhL9Cz6KFMsw8tRn0iSTO6Q=w914-h637-no?authuser=0"
                  {% endif %}
                  width="50%"
                  style="display: block; border: 0px; min-width: 220px"
                  alt="Thumbnail Image"
                />

              </td>
            </tr>
          </table>
        </td>
      </tr>
      <tr>
        <td bgcolor="#f4f4f4" align="center" style="padding: 0px 10px 0px 10px">
          <table
            border="0"
            cellpadding="0"
            cellspacing="0"
            width="100%"
            style="max-width: 600px"
          >
            <tr>
              <!--prettier-ignore-->
              <td
                bgcolor="#ffffff"
                align="center"
                style="
                  padding: 20px 20px 20px 20px;
                  color: #666666;
                  font-family: 'Lato', Helvetica, Arial, sans-serif;
                  font-size: 22px;
                  font-weight: 400;
                  line-height: 25px;
                "
              >
                <p style="margin: 0">
                  {% if rating_change.newRank != rating_change.oldRank and rating_change.newRating > rating_change.oldRating %}
                    Congratulations on becoming
                    <span style="color: #b92895; font-weight: 600; text-transform: capitalize;">{{rating_change.newRank}}</span>!!
                  {% elif rating_change.newRating > rating_change.oldRating %}
                    We are happy to inform that your rating has been
                    <span style="color: #b92895; font-weight: 600">Increased</span>!!
                  {% elif rating_change.newRating < rating_change.oldRating %}
                    We are sorry to inform that your rating has been
                    <span style="color: #b92895; font-weight: 600">Dropped</span>!!
                  {% else %}
                    Your rating has been
                    <span style="color: #b92895; font-weight: 600">Unchanged</span>!!
                  {% endif %}
                </p>
              </td>
            </tr>
            <tr>
              <td
                bgcolor="#ffffff"
                align="center"
                style="
                  font-family: 'Lato', Helvetica, Arial, sans-serif;
                  font-size: 22px;
                  font-weight: 400;
                  line-height: 25px;
                "
              >
                <table width="100%" border="0" cellspacing="0" cellpadding="0">
                  <tr>
                    <td
                      bgcolor="#ffffff"
                      align="center"
                      style="
                        padding: 10px 30px 40px 30px;
                        display: flex;
                        justify-content: space-around;
                        align-items: center;
                      "
                    >
                      <table border="0" cellspacing="0" cellpadding="0">
                        <tr
                          style="display: flex; justify-content: space-around"
                        >
                          {% if rating_change.oldrating == 0 %}
                          <div
                            align="right"
                            style="
                              color: #666666;
                              font-weight: 600;
                              padding: 5px;
                              display: inline-block;
                              flex-grow: 1;
                              flex-basis: 0;
                              text-transform: capitalize;
                            "
                          >
                            <span class="user-black">Unrated</span>
                          </div>
                          {% else %}
                          <div
                            align="right"
                            style="
                              color: #666666;
                              font-weight: 600;
                              padding: 5px;
                              display: inline-block;
                              flex-grow: 1;
                              flex-basis: 0;
                              text-transform: capitalize;
                            "
                          >
                            {{rating_change.oldRating}}<br/>
                            <span class="{{rating_change.oldcolor}}">
                              {{rating_change.oldRank}}
                            </span>
                          </div>
                          {% endif %}
                          <div
                            style="
                              color: #666666;
                              font-weight: 600;
                              padding: 5px;
                              display: inline-block;
                              flex-grow: 1;
                              flex-basis: 0;
                            "
                          >
                            <img
                              style="width: 100px"
                              border="0"
                              src="https://lh3.googleusercontent.com/BwKyLeLDkS4yXtCZaCI4VoOiWHQj3CzaxgqZefAk1IY30cS50BeJtcPIsUE9tlZVM7A9YOc5egNelw45OhJeO-NKgq78fyzfYTOjvC23Qhdeqc7TNGvdr3X7fvpk_JrLF-4R09joLAmG4ljHHjDUlMVRFqigL_V3lO2SXsBXtRQS937_607_PDh2A7c8ClgQoXvxa_K-H8OMS7NdgRMiFJqXNuX3GcMSdvBEo9Y3NoCQtm2kKoMZjI8yfRcG_cb-5Pjd7bvZNSbiLb-ekZMSkqEcm-AqoNwgxSBeARF0k_BHKJqD7XNZA1q5Mx9z7F3E9s3myY9wYTiD-Vq6a88OwYw472ucIBS30B07XgKJFaNzEmCvSaYCZ4MRxorHOSLYAJbqt7gdDVYn8j2pJpM4IqZ8-Rf651vxYtcSusguEnz05vHZ7Xh1nkdjb7Me__sNLskb5dF7SX3WoqbalnrMHKZCb_N6gFsms3h6BVu-UjOJANjjce1eCRc7MU8v1rCwCbZEq6TNcmpuEGgtXnxdVlK9ijuYhHim3G__qPlvlwPyAlXG81NHmFrv1V9uQfDQI9yafCZVGujWAjzyxB4Il0cWKRV2aJP3ZdtbFVdajfIE2G7Tm0hAONubMToMnsNevPmwOpu04Gs1-BolYpyrJdzfIfGSjsOU0o1EVFf1oRdkwt-L3E15bZg-METYbO4K1BLQY_Z-EH08UD90NR7QK5c=w220-h163-no?authuser=0"
                              alt="to"
                            />
                          </div>
                          <div
                            align="left"
                            style="
                              font-weight: 600;
                              padding: 5px;
                              color: #666666;
                              flex-grow: 1;
                              display: inline-block;
                              flex-basis: 0;
                              text-transform: capitalize;
                            "
                          >
                            {{rating_change.newRating}} <br />
                            <span class="{{rating_change.newcolor}}">
                              {{rating_change.newRank}}
                            </span>
                          </div>
                        </tr>
                      </table>
                    </td>
                  </tr>
                </table>
              </td>
            </tr>
            <!-- COPY -->
            <tr>
              <td
                bgcolor="#ffffff"
                align="center"
                style="
                  padding: 0px 25px;
                  color: #666666;
                  font-family: 'Lato', Helvetica, Arial, sans-serif;
                  font-size: 20px;
                  font-weight: 400;
                  line-height: 25px;
                "
              >
                <div
                  style="
                    max-width: 350px;
                    padding: 10px;
                    border: 1px solid #ffa73b;
                    border-radius: 4px;
                    border-top: 3px solid #ffa73b;
                  "
                >
                  <span style="color: #ffa73b; font-weight: 500"
                    >Your Standings</span
                  >
                  <div style="padding: 10px 0 0 0">
                    <span style="font-size: 16px">
                      World Rank - {{cdata.worldRank}} /
                      {{cdata.contest.participants}}</span
                    ><br />
                    <span style="font-size: 16px">
                      Country Rank - {{cdata.countryRank}} /
                      {{cdata.totalCountryParticipants}}</span
                    ><br />
                    <span style="font-size: 16px">
                      Organization Rank - {{cdata.organizationRank}} /
                      {{cdata.totalOrganizationParticipants}}</span
                    >
                  </div>
                </div>
              </td>
            </tr>
            {% if not rating_change.newRating > rating_change.oldRating %}
            <tr>
              <td
                bgcolor="#ffffff"
                align="center"
                style="
                  padding: 20px 10px 0px 10px;
                  color: #666666;
                  font-family: 'Lato', Helvetica, Arial, sans-serif;
                  font-size: 20px;
                  font-weight: 400;
                  line-height: 24px;
                "
              >
                <h5 style="margin: 0; max-width: 300px">
                  "Never let the fear of striking out keep you from playing the
                  game🙂"
                </h5>
              </td>
            </tr>
            {% endif %}
            <!-- COPY -->
            <tr>
              <td
                bgcolor="#ffffff"
                align="left"
                style="
                  padding: 20px 30px;
                  color: #666666;
                  font-family: 'Lato', Helvetica, Arial, sans-serif;
                  font-size: 15px;
                  font-weight: 400;
                  line-height: 25px;
                "
              >
                <p style="margin: 0">
                  Finally, keep track of your motivations, whatever it is that
                  you hope to get out of the experience. Good luck and have
                  fun!!
                </p>
              </td>
            </tr>
            <tr>
              <td
                bgcolor="#ffffff"
                align="left"
                style="
                  padding: 0px 30px 40px 30px;
                  border-radius: 0px 0px 4px 4px;
                  color: #666666;
                  font-family: 'Lato', Helvetica, Arial, sans-serif;
                  font-size: 15px;
                  font-weight: 400;
                  line-height: 25px;
                "
              >
                <p style="margin: 0">Cheers,<br />Codedigger Team</p>
              </td>
            </tr>
          </table>
        </td>
      </tr>
      <tr>
        <td
          bgcolor="#f4f4f4"
          align="center"
          style="padding: 30px 10px 0px 10px"
        >
          <table
            border="0"
            cellpadding="0"
            cellspacing="0"
            width="100%"
            style="max-width: 600px"
          >
            <tr>
              <td
                bgcolor="#FFECD1"
                align="center"
                style="
                  padding: 30px 30px 30px 30px;
                  border-radius: 4px 4px 4px 4px;
                  color: #666666;
                  font-family: 'Lato', Helvetica, Arial, sans-serif;
                  font-size: 18px;
                  font-weight: 400;
                  line-height: 25px;
                "
              >
                <h2
                  style="
                    font-size: 20px;
                    font-weight: 400;
                    color: #111111;
                    margin: 0;
                  "
                >
                  Need more help?
                </h2>
                <p style="margin: 0">
                  <a
                    href="mailto:contact.codedigger@gmail.com"
                    target="_blank"
                    style="color: #ffa73b"
                    >We&rsquo;re here to help you out</a
                  >
                </p>
              </td>
            </tr>
          </table>
        </td>
      </tr>
      <tr>
        <td bgcolor="#f4f4f4" align="center" style="padding: 0px 10px 0px 10px">
          <table
            border="0"
            cellpadding="0"
            cellspacing="0"
            width="100%"
            style="max-width: 600px"
            bgcolor="#f4f4f4"
          >
            <tr>
              <td
                align="center"
                style="
                  padding: 0px 30px;
                  color: #666666;
                  font-family: 'Lato', Helvetica, Arial, sans-serif;
                  font-size: 14px;
                  font-weight: 400;
                  line-height: 18px;
                "
              >
                <br />
                <p style="margin: 0">
                  If these emails get annoying, mail us to
                  <a
                    href="mailto:contact.codedigger@gmail.com"
                    target="_blank"
                    style="color: #111111; font-weight: 700"
                    >unsubscribe</a
                  >.
                </p>
              </td>
            </tr>
            <tr align="center">
              <th
                class="column_shop_social_icons"
                width="100%"
                style="padding: 0 0 20px 0"
                align="center"
              >
                <a
                  class="social-link"
                  href="https://discord.gg/4ZeNgUn7cF"
                  target="_blank"
                  title="Codedigger Discord"
                  style="
                    color: #ecba78;
                    text-decoration: none !important;
                    font-size: 14px;
                    text-align: center;
                  "
                >
                  <img
                    class="social-icons"
                    alt="Discord"
                    src="https://lh3.googleusercontent.com/DSHo9VjeqLhvFHXZTyJbTAsus9cj6kuWg-Pe7SFIUp2_NHSW9J1kJEkvFcX5An29Bhbjg9gjD6cbMM34ivKhTuqHq-CIQs2LzF3oKyEmhho4eKZ_EFI8gq9QVdWyY6HHY_HkJlinV8ZrWhvmjHo_3iD0bpFKO82XmDHubi1XP4N92ojhU_uSTC8D1jLAZqOm6pLZzu4wep4tzj0QQaG_7S3_1Rvz3K3tpc3anlk4cpp7UsYmC0s7deZ_ixlW2PPm_N8FDR4FKMvdJO43vEBpWF_A24nWRD1X9eGdfFQBhvD49FHmOhq6FZIxsJG3zguGUg6AxqtGTmPoIK-FTJSm82b0_dIhX8EvoVmtUIXscoFC34znIgiabEGXJ5Yod69E1O6s1iBEnmIno2X02XqfHirBRALD1vU6SF_fc1-bVVHf3aHHzd9bqD9ElQDht4hMACohjiG6RLjrbVU3JQVBBNnDNrw8es1X8ENxsir0VaTiXI5OTHvm5YMWo6r73EfKgRLe_wXuQiz2OcaIKuPGkfvW8R_grZ2ZnY6XyXD_3nmnOpRbZPwtx8D21fDyccaxoxAE6ik5dXvTvxvsG4POpMoYykFnxnlpr19IJEjvVW4qX9Tb8S6Zhn8q27C1HS94he0hY4UYXIL9e1n_vsK3q6o3rmmDpOOmREnrPWtViQvXQ14uYOz2kRVSouVRh3vPnq7nL11nlUFVImf0v82V47A=s24-no?authuser=0"
                    style="
                      height: auto !important;
                      vertical-align: middle;
                      text-align: center;
                      padding: 6px 6px 0;
                    "
                  />
                </a>
                <a
                  class="social-link"
                  href="https://www.linkedin.com/company/codedigger"
                  target="_blank"
                  title="Codedigger Linkedin"
                  style="
                    color: #ecba78;
                    text-decoration: none !important;
                    font-size: 14px;
                    text-align: center;
                  "
                >
                  <img
                    class="social-icons"
                    alt="Linkedin"
                    src="https://lh3.googleusercontent.com/y2FcyF-YK9xNG1VnXdV09ujmWsL5HmSn6-0e5vMQ6ZoxB7rYNkCsJUBZGPEOCRexPKXz0w29h7qEhb43BXP0sdQcCSoLF6XnRupcxOMeQCOtupDTjnT4PcKTHnhaayoINzWYhHbp_aGhCnl95DgOVVeDdBTY8Bz-_7kodiTioh1BSRtsUofNkjL36IMYeh35oplZfdG_je_IxWR1Ib97xuGZT_gFOW9BOFV9meV3eIuang--mMXtlWSkCEPBju9dUMdjbvXTx78j55Jb0O3HEqdTRTC1G-oxaJ-HtHZKj5oH75qEC9gJ8lVkHwvlhRPFgA-JZkmesNaDY0k_iJvMjRmQa9aLqod_Z88ruLHDZuDriwXCvL6RE1E0woW4RDX6P8lG5pccReOa2B-PMUCLFMpz9E-pVk87RbV9kK1Oo35L-4RhCN-WBcVvrpA_h5ttEnzchTiZg5ZgSasD6STtw8prmM9iF6gnN-qwIMU9x8yWed72dLOnN-nnf4EtTgnojNOghtIhJ5lfa4Wyw1eKG0ifBAwIF9W2Dougj3gjZGOUI9NcI0tBgnAYGYVPVW3IWPcABZ8b1uF3-GLr-sCMQU0o5-F2JlsvlL2xj1kuRjo-0A7d-e8gz0xgGYsrnhDjAHFhJoNqeJqt2W9O6YzNdAAPHybRcemTfXpsrkF_o8dMhrsyT4LpKjVunJqAHvo6PMCXKGuGWYsa8fytsz2GxT0=s24-no?authuser=0"
                    style="
                      height: auto !important;
                      vertical-align: middle;
                      text-align: center;
                      padding: 6px 6px 0 0px;
                    "
                  />
                </a>
                <a
                  class="social-link"
                  href="https://www.youtube.com/channel/UCY5XRYpEGKT9cpzZmfWvh6A"
                  target="_blank"
                  title="Codedigger Youtube"
                  style="
                    color: #ecba78;
                    text-decoration: none !important;
                    font-size: 14px;
                    text-align: center;
                  "
                >
                  <img
                    class="social-icons"
                    alt="Youtube"
                    src="https://lh3.googleusercontent.com/pYqpwO7h8-75TYZyRBPOVGOUXKjRp4iZLDbwZI3XWalD6MI_ouV--BkaRc3llicgbqHeUBziIKOvoBWY8ZpisUm0yjz1d-YQLWTiMcldNfgZwasn9lqQMP7PgQrkyT9yzVpMzNJT0MDu-YLvspps_phQ-YQVR_cfBQ2hEOyZDsyI7ozR_tRA0Qz9bo7a1eW8eW36wqRQUaM6PyqBp27Ew3zsKoGkdyjdjIS_nvX4SJPbvH1WqDD4zBXUloqZHD5ympRopU5DQ_h4hkwz152ggRR6xAQRPFA2-fPiynua2Pi6GIuh80euFvLSjCbKw-OXZ22jG-rsh_eTPK8P2I1349MyVfSfgcWu74uvznLjJ-lDe-0ejaTnBdWEdctYx_bXQw0s8WfYRI05IOSM0a0wchkIPyKwUvzoHcvgvxV8phVKb_Y2dm3Tm3dbAHoJR1EbMb1pnJz-vrrPnYjFzKLGecdDWI3WiKFdvaS9yTieaDvoUTMsJoxpi5QsuT3g8rT1YAJC7DOp2OrubT1LlzphScqm5ayv5TdIo1Gi97sWqqq0uKRkFyz8peNVVqbw0hX1pc2wYhoarFfq6YbzWS5KUOS0NN_zWuZsGunOAoEwwJLjIOGVFvotvaCdzQyhqBDs5je00C2_sJoAxHB5dhwYyBk2UXmAXSBIdTy6IaHlxtwzMaimBXhcnObuSXHl7q-1YTjIvBLLAanaBbEneHd6nzM=s24-no?authuser=0"
                    style="
                      height: auto !important;
                      vertical-align: middle;
                      text-align: center;
                      padding: 6px 6px 0;
                    "
                  />
                </a>
                <a
                  class="social-link"
                  href="https://www.facebook.com/practicewithcodedigger/"
                  target="_blank"
                  title="Codedigger Facebook"
                  style="
                    color: #ecba78;
                    text-decoration: none !important;
                    font-size: 14px;
                    text-align: center;
                  "
                >
                  <img
                    class="social-icons"
                    alt="Facebook"
                    src="https://lh3.googleusercontent.com/vTgkyeGkDVNIvA2h8mlyqjm1TKLXENdPeGUyQZ7sdUmpqYXnsMlRx8CDb5BaEgXaQylwlXlx5NZZvwaQqeEgrWBEhCNTXjNBFxmnpGCiWyQ67xj0_4FC0iVsxH4rHc0empC28OQr9mET4ZnxNnfzqoHsDFnq3lPPQBsyTUVVy-iGA1zRqLLqn54OkC0YhJ7Dhlx2PQB0B7ka_Z-6pDLj1_0qU90VD-ogxjXZeXbEpLQ5Jh0TYGaqjYi5Fsn5O9U_tI-aaHr9T5p6_VLlOdgAliUSVx-uhQiWXNjlD7FsWsC4lrb2N7eMmOX-ukpeJEnhxTsJmpNZJEgtw9bDQifDxJdhcP83nn-mZrFp0trpNKmJRd9GSH3t9uzuPkCzu2AZ7fJD75u6TPTOpbFYQpGf9EK31jYIHMwDnb22bgtdoGrnqu21QUIFEEygV7j7gblwhUWqEnPl8zHOeN3fhA5tPwNuTcKVc3UjkQyXZrnj7XV55vRe3bipxIUA5hd2CH9l4T8BkggNnikAplmdoxpGNXMsNUjkuxRk1EU3RR9CXPKiWU_OBsGqlsATIfMyvMCP_4MzneaVxbbTiqcJLW1ga6XNCJMLtAI2S-fKUsAZTh4iFDSTiihZMkSMtWD__1xdTa89gTsVXZ-zk33j2saTg8q5X1kNpDfZpi7UXjIzqvMnW2wR4LLyYOIQYqKmdHBtqpAzl2fvYUoE3Sym4idiO7Q=s24-no?authuser=0"
                    style="
                      height: auto !important;
                      vertical-align: middle;
                      text-align: center;
                      padding: 6px 6px 0;
                    "
                  />
                </a>
                <p
                  style="
                    color: #666666;
                    font-family: 'Lato', Helvetica, Arial, sans-serif;
                    font-size: 12px;
                    font-weight: 400;
                    line-height: 18px;
                  "
                >
                  © 2020 CODEDIGGER. All Rights Reserved.
                </p>
              </th>
            </tr>
          </table>
        </td>
      </tr>
    </table>
  </body>
</html>
"""
