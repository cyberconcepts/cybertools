/*
 * Copyright (c) 2009 Helmut Merz helmutm@cy55.de
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
 */

/*
 *
 * $Id$
 *
 */

dojo.provide('jocy.talk');


dojo.declare('jocy.talk.Connection', null, {

    info: 'jocy.talk Connection',
    constructor: function(url, client, user, password){
        this.url = url.replace(/\/$/, '');
        this.client = client;
        this.user = user;
        this.password = password;
        this._cometdInitialized = false;
    },
    initCometd: function() {
        if (!this._cometdInitialized) {
            dojox.cometd.init(this.url);
            this._cometdInitialized = true;
        }
    },
    unload: function(){
        if (this._cometdInitialized) {
            dojox.cometd.disconnect();
            this._cometdInitialized = false;
        }
    },

    // ReST methods
    get: function(resourcePath, data, cbName, user, password) {
        return dojo.xhrGet({
            url: this._setupUrl(resourcePath),
            load: function(response, ioArgs) {
                return this._callback(response, ioArgs, cbName);
            },
            content: data,
            handleAs: 'json',
            user: user,
            password: password
        });
    },
    getSynchronous: function(resourcePath, data, cbName) {
        var result = {};
        d = dojo.xhrGet({
            url: this._setupUrl(resourcePath),
            load: function(response, ioArgs) {
                result = response;
                return response;
            },
            content: data,
            handleAs: 'json',
            user: this.user,
            password: this.password,
            sync: true
        });
        return result;
    },
    put: function(resourcePath, data, cbName) {
        return dojo.xhrPut({
            url: this._setupU(cbName),
            load: function(response, ioArgs) {
                return this._callback(response, ioArgs, cbName);
            },
            putData: dojo.toJson(data),
        });
    },
    post: function(resourcePath, data, cbName) {
        return dojo.xhrGet({
            url: this._setupU(resourcePath),
            load: function(response, ioArgs) {
                return this._callback(response, ioArgs, cbName);
            },
            postData: dojo.toJson(data)
        });
    },
    rpc: function(resourcePath, methodName, data, cbName) {
        return this.post(resourcePath, {method: methodName, data: data}, cbName);
    },
    remove: function(resourcePath, cbName) {
        return dojo.xhrDelete({
            url: this._setupU(resourcePath),
            load: function(response, ioArgs) {
                return this._callback(response, ioArgs, cbName);
            },
        });
    },

    // cometd methods
    publish: function(channel, data) {
        this.initCometd();
        dojox.cometd.publish(channel, data);
    },
    subscribe: function(channel, cbName){
        this.initCometd();
        dojox.cometd.subscribe(channel, this.client, cbName);
    },

    // private methods
    _setupObjectPath: function(path) {
        slash = (path.charAt(0) == '/' ? '' : '/');
        return this.url + slash + path;
    },
    _callback: function(response, ioArgs, cbName) {
        this.client[cbName](response);
        return response;
    },

    /* dojox.cometd example */
    join: function(name) {
        if(name == null || name.length==0 ){
            alert('Please enter a username!');
        } else {
            this._username=name;
            dojox.cometd.startBatch();
            dojox.cometd.subscribe("/chat/demo", this, "_alert");
            dojox.cometd.publish("/chat/demo",
                    {user: this._username, join: true,
                     chat: this._username + " has joined"});
            dojox.cometd.endBatch();
            this._meta = dojo.subscribe("/cometd/meta", function(event) {
                console.debug(event);
            });
        }
    },
    _alert: function(data) {
        alert(data);
    },
});
