cd /usr/src/
wget https://raw.githubusercontent.com/romonzaman/newfies-dialer/develop/install/install-all.sh
bash install-all.sh

issues:
1. debug enable
2. redis correct version
pip install redis==2.10.6
3. disable redis cache.use file cache
4. 


 /etc/freeswitch/freeswitch/autoload_configs/lua.conf.xml
```
<configuration name="lua.conf" description="LUA Configuration">
  <settings>

    <!--
    Specify local directories that will be searched for LUA modules
    These entries will be pre-pended to the LUA_CPATH environment variable
    -->
    <!-- <param name="module-directory" value="/usr/lib/lua/5.1/?.so"/> -->
    <!-- <param name="module-directory" value="/usr/local/lib/lua/5.1/?.so"/> -->
    <param name="module-directory" value="/usr/lib/x86_64-linux-gnu/?.so"/>
    <param name="module-directory" value="/usr/lib/x86_64-linux-gnu/lua/5.2/?.so"/>
    <param name="module-directory" value="/usr/lib/x86_64-linux-gnu/lua/5.2/luasql/?.so"/>
    <param name="module-directory" value="/usr/lib/i386-linux-gnu/lua/5.2/?.so"/>
    <param name="module-directory" value="/usr/local/share/lua/5.2/?.so"/>
    <param name="module-directory" value="/usr/local/lib/lua/5.2/?.so"/>
    <param name="module-directory" value="/usr/local/lib/lua/5.2/luasql/?.so"/>

    <!--
    Specify local directories that will be searched for LUA scripts
    These entries will be pre-pended to the LUA_PATH environment variable
    -->
    <!-- <param name="script-directory" value="/usr/local/lua/?.lua"/> -->
    <!-- <param name="script-directory" value="$${base_dir}/scripts/?.lua"/> -->

    <!--<param name="xml-handler-script" value="/dp.lua"/>-->
    <!--<param name="xml-handler-bindings" value="dialplan"/>-->

    <!--
        The following options identifies a lua script that is launched
        at startup and may live forever in the background.
        You can define multiple lines, one for each script you
        need to run.
    -->
    <param name="startup-script" value="/usr/share/newfies-lua/listener.lua"/>
    <!--<param name="startup-script" value="startup_script_1.lua"/>-->
    <!--<param name="startup-script" value="startup_script_2.lua"/>-->
  </settings>
</configuration>

```
