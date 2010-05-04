/*
 * Copyright (c) 2010 Helmut Merz helmutm@cy55.de
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


// $Id$


dojo.provide('jocy.talk');


dojo.declare('jocy.talk.Connection', null, {

    info: 'jocy.talk Connection',

    constructor: function(url, name) {
        this.url = url;
        this.connected = false;
        this.receiver = null;
        this.receiving = false;
        this.id = (name == undefined | name == '' ? null : name);
    },

    connect: function() {
        return dojo.xhrPost({
            url: this.url + '/.talk/connect',
            postData: (this.id == null ? '' : dojo.toJson({name: this.id})),
            handleAs: 'json',
            error: dojo.hitch(this, this._handleError),
            load: dojo.hitch(this, function(response, ioArgs) {
                console.log(response);
                this.id = response.id;
                this.connected = true;
            })
        });
    },

    receive: function(timeout) {
        if (this.receiving) {
            return;
        }
        this.receiving = true;
        return dojo.xhrPost({
            url: this.url + '/.talk/receive/' + this.id,
            handleAs: 'json',
            error: dojo.hitch(this, this._handleReceiveError),
            load: dojo.hitch(this, this._handleReceiveResponse)
        });
    },

    send: function(receiver, data) {
        return dojo.xhrPost({
            url: this.url + '/.talk/send/' + receiver,
            postData: dojo.toJson(data),
            handleAs: 'json',
            error: dojo.hitch(this, this._handleError),
            load: dojo.hitch(this, function(response, ioArgs) {
                console.log(response);
            })
        });
    },

    disconnect: function() {
        this.connected = false;
        return dojo.xhrPost({
            url: '/.talk/disconnect/' + this.id,
            handleAs: 'json',
            error: dojo.hitch(this, this._handleError),
            load: dojo.hitch(this, function(response, ioArgs) {
                console.log(response);
                this.receiving = false;
            })
        });
    },

    // private methods

    _handleReceiveResponse: function(response, ioArgs) {
        console.log(response);
        if (!this.receiving) {
            return;
        }
        this.receiving = false;
        st = response.state;
    },

    _handleReceiveError: function(response, ioArgs) {
        console.log(response);
        if (!this.receiving) {
            return;
        }
        this.receiving = false;
        //this._poll();
    },

    _handleError: function(response, ioArgs) {
        console.log(response);
    }

});

