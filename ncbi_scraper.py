from __future__ import division

from Bio import Entrez

def main():
    ncbi_searcher()

def ncbi_searcher(term_string='Fatty Liver Disease'):
    '''
    Function to get a list of PMIDs and there datasets. Making a script to do this is neccessary because some papers have relevant datasets but no accession listed. I found this out by trying trying to use the paper PMID27028797 as case in which interesting omics was done,
    but no datasets were depositited. There was a link to the SRA dataset from pubmed listed
    but this would be too tedious to do by hand.
    '''
    Entrez.email = 'lefeverde@pitt.edu'
    ehandle = Entrez.esearch(db='pubmed', term=term_string, retmode='xml', retmax=100000000)
    edict = Entrez.read(ehandle)
    pmid_list = edict['IdList']

    sra_handle = Entrez.elink(dbfrom='pubmed',db='sra',retmax=100000000, id=pmid_list, retmode='xml')
    sra_recs = Entrez.read(sra_handle)
    with open('fld_pmids_and_sras.txt', 'w+') as out_file:
        for cur_rec in sra_recs:
            try:
                cur_pmid = cur_rec['IdList'][0]
                link_dict = cur_rec['LinkSetDb'][0]['Link']
                id_link_list = [i['Id'] for i in link_dict]

                if len(id_link_list) > 5:
                    link_id_str = ''
                    for i in id_link_list:
                        link_id_str += i + ','
                    link_id_str = link_id_str.strip(',') # kludge but whatever
                    out_file.write(cur_pmid + ';' + link_id_str + '\n')

            except IndexError:
                continue

            #cur_pmid = cur_rec['IdList']
            #link_dict = cur_rec['LinkSetDb']['Link']



if __name__ == '__main__':
    main()
