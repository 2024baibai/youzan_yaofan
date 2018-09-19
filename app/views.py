#-*- coding=utf-8 -*-
from app import app, db
from flask import render_template, make_response, redirect, request, url_for, flash, session, jsonify, g, current_app, send_from_directory
import urllib
import re
import os



@app.route('/sitemap.xml', methods=['GET'])
def sitemap():
    """Generate sitemap.xml. Makes a list of urls and date modified."""
    pages = []
    ten_days_ago = (datetime.now() - timedelta(days=10)
                    ).strftime('%Y-%m-%d %H:%M:%S')
    # static pages
    for rule in current_app.url_map.iter_rules():
        if "GET" in rule.methods and len(rule.arguments) == 0:
            pages.append([rule.rule, ten_days_ago])

    sitemap_xml = render_template('sitemap_template.xml', pages=pages)
    response = make_response(sitemap_xml)
    response.headers["Content-Type"] = "application/json"

    return response


@app.route('/robots.txt', methods=['GET'])
def robots():
    robots = render_template('robots.txt')
    response = make_response(robots)
    response.headers["Content-Type"] = "text/plain"
    return response


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')
