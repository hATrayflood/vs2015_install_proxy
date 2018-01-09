vs2015_install_proxy
====================
Local proxy server for Visual Studio 2015 installing.

Issue
-----
https://social.msdn.microsoft.com/Forums/ja-JP/44e680ee-5863-460b-b03c-6e259d6774af/visual-studio-2015?forum=vsgeneralja

How to use
----------
1. Install Python 3.6.*
    * https://www.python.org/downloads/release/python-364/
2. Start proxy server
    * Fix python path to your environment.
    * ```vs2015_install_proxy.bat```
3. Set Auto-Proxy Configuration Script
    * ```http://localhost:8080/proxy.pac```
5. Run Visual Studio 2015 Installer
    * ```ja_visual_studio_community_2015_with_update_3_x86_x64_web_installer_8922964.exe /layout```

if access log not appeared in console, restart Windows.

github
------
https://github.com/hATrayflood/vs2015_install_proxy

License
-------
Microsoft Public License (MS-PL)  
https://opensource.org/licenses/MS-PL  
