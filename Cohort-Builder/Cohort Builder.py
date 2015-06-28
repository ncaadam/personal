from __future__ import division
from flask import Flask, Response, request, jsonify
from neo4jrestclient.client import GraphDatabase
from neo4jrestclient.constants import RAW
import graphlab as gl
import pandas as p
import json

app = Flask(__name__)

db = GraphDatabase('http://localhost:7474', username='neo4j', password='neo')


@app.route('/')
def landing_page():
    resp = Response({}, status=200, mimetype='application/json')
    return resp


@app.route('/_api/v1/cohort/', methods=['GET'])
def get_cohort():
    path_list = []
    filter_list = []
    filters = False

    # PROVIDER TYPE QUERY BUILDER
    provider_type = request.args.getlist('pt')
    if len(provider_type) > 0:
        filters = True
        pt_tf = True
        path_list.append("(p:Provider)-->(s:Specialty)")
        provider_type = provider_type[0].split(',')
        pt_str = "['" + "','".join(str(pt) for pt in provider_type) + "']"
        pt_cy = "(s.specialty IN " + pt_str + ")"
        filter_list.append(pt_cy)
    else:
        pt_tf = False
        pt_cy = ""

    # HCPCS QUERY BUILDER
    hcpcs = request.args.getlist('hcpcs')
    if len(hcpcs) > 0:
        filters = True
        hcpcs_tf = True
        path_list.append("(p:Provider)-->(h:HCPCS_Code)")
        hcpcs = hcpcs[0].split(',')
        hcpcs_str = "['" + "','".join(str(hcpc) for hcpc in hcpcs) + "']"
        hcpcs_cy = "(h.hcpcs_codeID IN " + hcpcs_str + ")"
        filter_list.append(hcpcs_cy)
    else:
        hcpcs_tf = False
        hcpcs_cy = ""

    # GEO QUERY BUILDER
    # this only uses zip codes right now
    geo = request.args.getlist('geo')
    if len(geo) > 0:
        filters = True
        geo_tf = True
        geo = geo[0].split(',')
        path_list.append("(p:Provider)")
        geo_str = "['" + "','".join(str(z) for z in geo) + "']"
        geo_cy = "(left(p.nppes_provider_zip,5) IN " + geo_str + ")"
        filter_list.append(geo_cy)
    else:
        geo_tf = False
        geo_cy = ""

    # HOSPITAL AFFILIATION QUERY BUILDER
    affiliation = request.args.get('aff', '', type=str)
    if affiliation is not '':
        filters = True
        aff_tf = True
        path_list.append("(p:Provider)-[:Hospital_Affiliation]->(e:Entity)")
        affiliation = "\"" + affiliation + "\""
        aff_cy = "(e.entity_name = " + affiliation + ")"
        filter_list.append(aff_cy)
    else:
        aff_tf = False
        aff_cy = ""

    # HOSPITAL OWNERSHIP BY QUERY BUILDER
    ownership = request.args.get('own', '', type=str)
    if ownership is not '':
        filters = True
        own_tf = True
        path_list.append("(p:Provider)-[:Hospital_Ownership]->(e2:Entity)")
        ownership = "\"" + ownership + "\""
        own_cy = "(e2.entity_name = " + ownership + ")"
        filter_list.append(own_cy)
    else:
        own_tf = False
        own_cy = ""

    # PGP QUERY BUILDER
    pgp = request.args.get('pgp', '', type=str)
    if pgp is not '':
        filters = True
        pgp_tf = True
        path_list.append("(p:Provider)-[:PGP_Affiliation]->(e3:Entity)")
        pgp = "\"" + pgp + "\""
        pgp_cy = "(e3.entity_name = " + pgp + ")"
        filter_list.append(pgp_cy)
    else:
        pgp_tf = False
        pgp_cy = ""

    # COMPANY QUERY BUILDER
    comp = request.args.get('comp', '', type=str)
    if comp is not '':
        filters = True
        comp_tf = True
        path_list.append("(p:Provider)-[:Part_of_Company]->(e4:Entity)")
        comp = "\"" + comp + "\""
        comp_cy = "(e4.entity_name = " + comp + ")"
        filter_list.append(comp_cy)
    else:
        comp_tf = False
        comp_cy = ""

    # IPA QUERY BUILDER
    ipa = request.args.get('ipa', '', type=str)
    if ipa is not '':
        filters = True
        ipa_tf = True
        path_list.append("(p:Provider)-[:Part_of_IPA]->(e5:Entity)")
        ipa = "\"" + ipa + "\""
        ipa_cy = "(e5.entity_name = " + ipa + ")"
        filter_list.append(ipa_cy)
    else:
        ipa_tf = False
        ipa_cy = ""

    # TODO: FUTURE FILTERS NOT YET AVAILABLE IN THE DATA
    # specialty = request.args.getlist('specialty')
    # specialty = specialty[0].split(',')
    # year = request.args.get('year', '2012', type=str)

    """
    example URL that should work, returning 7 nodes
    http://localhost:5001/_api/v1/cohort/?pt=Internal%20Medicine&geo=60614,60615&hcpcs=99205
    """

    # BUILD THE WHOLE QUERY
    # a node is the Provider node, b node is the provider_type node, c node is the hcpcs_code node
    if filters:
        start_q = "MATCH " + ",".join(path for path in path_list) + " WHERE "
        where_q = " AND ".join(filt for filt in filter_list)
        end_q = " RETURN DISTINCT p"
        q = start_q + where_q + end_q
    else:
        q = "MATCH (n:Provider)-[r:Refers_To]-(b:Provider) RETURN DISTINCT b,n LIMIT 100"

    print q

    # call the query
    params = {}
    query_sequence_object = db.query(q, params=params, returns=RAW)

    # get the number of nodes it responded with
    resp_len = len(query_sequence_object)
    print resp_len

    """
    node_list = []
    for node in query_sequence_object:
        n = node.pop()
        data = n.get('data')
        metadata = n.get('metadata')
        print metadata
        node_list.append(data)
    """

    # initialize response dictionary, with the number of nodes and the query used to hit neo4j
    json_response = dict(node_count=resp_len, cypher_query=q)

    # go through every node and get that data associated with node and put it in a list
    node_list = []
    for pair in query_sequence_object:
        n = pair.pop()
        n_dict = dict(node_id=n['metadata']['id'], node_data=n['data'])
        node_list.append(n_dict)

    json_response['nodes'] = node_list

    # build the response in json with the list of data you have
    resp = Response(json.dumps(json_response), status=200, mimetype='application/json')

    # send back the response that was built
    return resp


@app.route('/_api/v1/network/', methods=['POST'])
def get_network():
    temp = request.data
    node_json = json.loads(temp)
    print node_json['node_count']
    # test_cohort = [19530, 2521, 17358, 2705, 13283, 1194, 17029, 2743, 1446, 21455, 10617, 1639,
    #               1014, 17672, 9866]

    node_list = []
    for node in node_json['nodes']:
        node_list.append(node['node_id'])

    print node_list
    cohort_string = "[" + ",".join(str(z) for z in node_list) + "]"
    q = "MATCH (p:Provider)<-[r1:Refers_To]->(p2:Provider) " \
        "WHERE (id(p) IN " + cohort_string + " AND id(p2) IN " + cohort_string + ") " \
                                                                                 "RETURN DISTINCT r1"
    print q

    # call the query
    params = {}
    query_sequence_object = db.query(q, params=params, returns=RAW)

    # get the number of nodes it responded with
    resp_len = len(query_sequence_object)
    print resp_len

    # create the relationships dictionary
    rels_dict = dict(cypher_query=q)
    rel_count = 0
    rel_list = []
    for x in query_sequence_object:
        r = x[0]
        r_data = r['data']
        r_start = r['start'][r['start'].rfind('/') + 1:]
        r_end = r['end'][r['end'].rfind('/') + 1:]
        r_id = r['self'][r['self'].rfind('/') + 1:]
        rel_entry = dict(relationship_id=r_id, start=r_start, end=r_end, data=r_data)
        rel_list.append(rel_entry)
        rel_count += 1

    rels_dict['relationship_count'] = rel_count
    rels_dict['relationships'] = rel_list

    nodes_rels = dict(nodes=node_json, relationships=rels_dict)

    # build the response in json with the list of data you have
    resp = Response(json.dumps(nodes_rels), status=200, mimetype='application/json')

    # send back the response that was built
    return resp


@app.route('/_api/v1/metrics/', methods=['POST'])
def get_metrics():
    # get the posted JSON data (nodes and rels)
    temp = request.data

    # load it into JSON
    n_r_json = json.loads(temp)

    # separate nodes and rels
    rels = n_r_json['relationships']
    nodes = n_r_json['nodes']

    # initialize pandas DF and bring the relationship data into it
    rels_p_df = p.DataFrame(columns=['data', 'end', 'relationship_id', 'start'])
    for rel in rels['relationships']:
        rels_p_df = rels_p_df.append(p.io.json.read_json(json.dumps(rel)))

    # create a list of all the node IDs
    node_list = []
    for node in nodes['nodes']:
        node_list.append(node['node_id'])

    # use the list of node IDs to create a pandas DF
    nodes_p_df = p.DataFrame(columns=['node_id'])
    nodes_p_df['node_id'] = node_list

    # convert the Pandas DFs to GL DFs
    nodes_g_df = gl.SFrame(nodes_p_df)
    rels_g_df = gl.SFrame(rels_p_df)

    # make all of the columns integer types as they're brought in as strings
    for col in rels_g_df.column_names():
        rels_g_df[col] = rels_g_df[col].astype(int)

    # initialize SGraph in GL and add the nodes and edges
    gl_graph = gl.SGraph()
    gl_graph = gl_graph.add_vertices(nodes_g_df, vid_field='node_id')
    gl_graph = gl_graph.add_edges(rels_g_df, src_field='start', dst_field='end')

    # run kcore graph analysis
    kc = gl.kcore.create(gl_graph, verbose=False)
    gl_graph.vertices['core_id'] = kc['graph'].vertices['core_id']

    # run pagerank graph analysis
    pr = gl.pagerank.create(gl_graph, verbose=False)
    gl_graph.vertices['pagerank'] = pr['graph'].vertices['pagerank']
    gl_graph.vertices['pagerank_delta'] = pr['graph'].vertices['delta']

    # run connected components graph analysis
    cc = gl.connected_components.create(gl_graph, verbose=False)
    gl_graph.vertices['component_id'] = cc['graph'].vertices['component_id']

    # run the triangle count graph analysis
    tc = gl.triangle_counting.create(gl_graph, verbose=False)
    gl_graph.vertices['triangle_count'] = tc['graph'].vertices['triangle_count']

    # get the in degrees and out degrees for each node
    def count_degrees(src, edge, dst):
        dst['in_degree'] += 1
        src['out_degree'] += 1
        return src, edge, dst

    def get_degree(g):
        new_g = gl.SGraph(g.vertices, g.edges)
        new_g.vertices['in_degree'] = 0
        new_g.vertices['out_degree'] = 0
        new_g = gl.SGraph(new_g.triple_apply(count_degrees, ['in_degree']).get_vertices(), g.edges)
        new_g = gl.SGraph(new_g.triple_apply(count_degrees, ['out_degree']).get_vertices(), g.edges)
        return new_g.get_vertices()

    # run the degree getting functions which return vertices
    gl_graph = gl_graph.add_vertices(get_degree(gl_graph), vid_field='__id')

    # add the metrics data to the nodes / rels json
    for v in gl_graph.get_vertices():
        for n in nodes['nodes']:
            if n['node_id'] == v['__id']:
                n['metrics'] = v

    # create JSON response with nodes and rels (including metrics)
    resp = Response(json.dumps(n_r_json), status=200, mimetype='application/json')

    # return the response
    return resp


@app.route('/_api/v1/provider/', methods=['GET', 'POST'])
def get_provider():
    # initialize Provider ID list
    provider_ids = []

    # metrics variables
    metrics_tf = False
    metrics_dict = {}

    # determine whether the request was a GET or a POST. Pull the IDs depending on each case
    # GET requests will send in 'node_id's
    if request.method == 'GET':
        raw_p_ids = request.args.getlist('p_id')
        provider_ids = raw_p_ids[0].split(',')

    # POST requests will post nodes JSON. This should be JSON that comes from the 'cohort' route
    # TODO: Accept JSON from the 'network' route as well
    # we could force the user to pass the correct JSON from the 'network' route themselves
    elif request.method == 'POST':
        temp = request.data
        node_json = json.loads(temp)
        for node in node_json['nodes']:
            if 'metrics' in node.keys():
                metrics_tf = True
                metrics_dict[node['node_id']] = node['metrics']
            provider_ids.append(node['node_id'])

    # this is a test set of IDs that can be used for testing purposes
    # test_cohort = [19530, 2521, 17358, 2705, 13283, 1194, 17029, 2743, 1446, 21455, 10617, 1639,
    # 1014, 17672, 9866]

    # initialize the list for each Provider's JSON data
    provider_list = []

    # loop through each Provider ID
    for provider in provider_ids:
        # for every Provider ID, create and execute the Cypher query
        # the cypher query looks for all the relationships that the Provider has except for the 'Refers_To' relationship
        # this is because the provider data is disbursed among other nodes via connections
        q = "START p=node(" + str(provider) + ") MATCH (p)-[r]->(n) WHERE type(r)<>'Refers_To' RETURN p,n,r"
        params = {}
        query_sequence_object = db.query(q, params=params, returns=RAW)

        # initialize the provider dictionary which will contain the relevant data
        provider_dict = {}

        # the response from neo4j is a list of provider node[0], connected node[1], relationship[2] between the two
        # loop through all the relationships that the Provider is connected to
        for rel in query_sequence_object:
            # grab the other node, the label for that node, and the data associated with it
            other_node = rel[1]
            label = other_node['metadata']['labels'][0]
            data = other_node['data']

            # grab the relationship between the Provider and the other node, the data on the relationships
            # and the type of relationship it is
            rel_data = rel[2]['data']
            rel_type = rel[2]['metadata']['type']
            rel_data.update({unicode('relationship_type'): rel_type})

            # if there is data in the relationship, append it to the other node data
            if rel_data != {}:
                data.update(rel_data)

            # if the other node label isn't a key in our provider dictionary yet, add it as a blank list
            # either way, append the data to that label's value (a list)
            if label not in provider_dict:
                provider_dict[label] = []
                provider_dict[label].append(data)
            else:
                provider_dict[label].append(data)

        # update the dollar flow for each HCPCS code, then the total_dollar_flow for the whole provider
        if 'HCPCS_Code' in provider_dict:
            total_dollar_flow = 0
            total_patients = 0
            total_new_patients = 0
            new_patient_codes = ['99201', '99202', '99203', '99204', '99205']

            for hcpcs in provider_dict['HCPCS_Code']:
                dollar_flow = float(hcpcs['line_srvc_cnt']) * float(hcpcs['average_Medicare_allowed_amt'])
                total_dollar_flow += dollar_flow
                hcpcs.update({'dollar_flow': unicode(dollar_flow)})
                total_patients += int(hcpcs['bene_unique_cnt'])
                if hcpcs['hcpcs_codeID'] in new_patient_codes:
                    total_new_patients += int(hcpcs['bene_unique_cnt'])

            # calculate the new patient percentage
            new_patient_perc = float(total_new_patients/total_patients)

            provider_dict.update({'total_dollar_flow': unicode(total_dollar_flow),
                                  'new_patient_percentage': unicode(new_patient_perc),
                                  'number_of_patients': unicode(total_patients),
                                  'number_of_new_patients': unicode(total_new_patients)})
        # make your JSON for this one Provider ID, adding the original node data, additional data, the node id,
        # and the cypher query used
        if metrics_tf:
            provider_json = dict(node_id=query_sequence_object[0][0]['metadata']['id'],
                                 node_data=query_sequence_object[0][0]['data'],
                                 metrics=metrics_dict[query_sequence_object[0][0]['metadata']['id']],
                                 additional_data=provider_dict,
                                 cypher_query=q)
        else:
            provider_json = dict(node_id=query_sequence_object[0][0]['metadata']['id'],
                                 node_data=query_sequence_object[0][0]['data'],
                                 additional_data=provider_dict,
                                 cypher_query=q)

        # add this json to the Provider list
        provider_list.append(provider_json)

    # dump the Provider list into a JSON dictionary with nodes and node_count
    final_provider_json = json.dumps(dict(nodes=provider_list, node_count=len(provider_list)))

    # generate the JSON response with the JSON generated
    resp = Response(final_provider_json, status=200, mimetype='application/json')

    # return the response to the client
    return resp


@app.route('/_api/v1/neighbors/', methods=['POST'])
def get_neighbors():
    temp = request.data
    node_json = json.loads(temp)
    # test_cohort = [19530, 2521, 17358, 2705, 13283, 1194, 17029, 2743, 1446, 21455, 10617, 1639,
    #                1014, 17672, 9866]

    node_list = []
    for node in node_json['nodes']:
        node_list.append(node['node_id'])

    cohort_string = "[" + ",".join(str(z) for z in node_list) + "]"
    out_q = "MATCH (p:Provider)-[r1:Refers_To]->(p2:Provider) " \
            "WHERE (id(p) IN " + cohort_string + ") RETURN DISTINCT r1,p2"
    in_q = "MATCH (p:Provider)<-[r1:Refers_To]-(p2:Provider) " \
           "WHERE (id(p) IN " + cohort_string + ") RETURN DISTINCT r1,p2"

    print out_q

    # call the query
    params = {}
    out_query_sequence_object = db.query(out_q, params=params, returns=RAW)

    # call the query
    params = {}
    in_query_sequence_object = db.query(in_q, params=params, returns=RAW)

    # create the relationships dictionary
    out_rels_dict = dict(node_count=len(node_list), cypher_query=out_q)
    out_rel_count = 0
    out_rel_list = []
    out_nodes = []
    out_node_id_list = []
    for row in out_query_sequence_object:
        r = row[0]
        r_data = r['data']
        r_start = r['start'][r['start'].rfind('/') + 1:]
        r_end = r['end'][r['end'].rfind('/') + 1:]
        r_id = r['self'][r['self'].rfind('/') + 1:]
        rel_entry = dict(relationship_id=r_id, start=r_start, end=r_end, data=r_data)
        out_rel_list.append(rel_entry)
        out_rel_count += 1

        n = row[1]
        n_id = n['metadata']['id']
        if n_id not in out_node_id_list:
            out_node_id_list.append(n_id)
            n_data = n['data']
            n_entry = dict(node_id=n_id, data=n_data)
            out_nodes.append(n_entry)

    out_rels_dict['relationship_count'] = out_rel_count
    out_rels_dict['relationships'] = out_rel_list
    out_nodes_dict = dict(nodes=out_nodes, node_count=len(out_nodes))

    in_rels_dict = dict(node_count=len(node_list), cypher_query=in_q)
    in_rel_count = 0
    in_rel_list = []
    in_nodes = []
    in_node_id_list = []
    for row in in_query_sequence_object:
        r = row[0]
        r_data = r['data']
        r_start = r['start'][r['start'].rfind('/') + 1:]
        r_end = r['end'][r['end'].rfind('/') + 1:]
        r_id = r['self'][r['self'].rfind('/') + 1:]
        rel_entry = dict(relationship_id=r_id, start=r_start, end=r_end, data=r_data)
        in_rel_list.append(rel_entry)
        in_rel_count += 1

        n = row[1]
        n_id = n['metadata']['id']
        if n_id not in in_node_id_list:
            in_node_id_list.append(n_id)
            n_data = n['data']
            n_entry = dict(node_id=n_id, data=n_data)
            in_nodes.append(n_entry)

    in_rels_dict['relationship_count'] = in_rel_count
    in_rels_dict['relationships'] = in_rel_list
    in_nodes_dict = dict(nodes=in_nodes, node_count=len(in_nodes))

    nodes_rels = dict(in_nodes=in_nodes_dict, in_relationships=in_rels_dict,
                      out_nodes=out_nodes_dict, out_relationships=out_rels_dict, nodes=node_json)

    # build the response in json with the list of data you have
    resp = Response(json.dumps(nodes_rels), status=200, mimetype='application/json')

    # send back the response that was built
    return resp


@app.route('/_api/v1/docs/')
def get_documentation():
    message = {'doc_link:': 'https://drive.google.com/open?id=0B5VudqrtA4nUaEl6b3BqdEkxcDQ&authuser=0',
               'api_version': '1.0'}
    resp = jsonify(message)

    return resp


@app.errorhandler(404)
def not_found(error=None):
    message = {'status': 404, 'message': 'Not Found: ' + request.url}
    resp = jsonify(message)
    resp.status_code = 404

    return resp

if __name__ == '__main__':
    # app.run(port=5001, debug=True)
    app.run(host='0.0.0.0')
