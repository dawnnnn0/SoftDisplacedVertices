#!/usr/bin/env python

from __future__ import print_function

import click
import ROOT

@click.command()
@click.argument("input", type=click.Path(dir_okay=False, exists=True))
@click.option("--first", default=0)
@click.option("--number", default=-1)
@click.option("--genpart", default=False, is_flag=True)
def main(input, first, number, genpart):
    
    rfile = ROOT.TFile.Open(input, "READ")

    for ievent, event in enumerate(rfile.Events):
        if first > ievent:
            continue
        if number > 0 and first + number <= ievent:
            break
        if genpart:
           print("Event: {} GenPart: {}".format(ievent, event.nGenPart))
           for i in range(event.nSDVGenPart):
              print("! {:3d} ! {:3d} ! {:8d} {:6d} ! {:9.2f} {:9.2f} {:9.2f} !".format(
                i,
                event.SDVGenPart_genPartIdxMother[i],
                event.SDVGenPart_pdgId[i],
                event.SDVGenPart_status[i],
                event.SDVGenPart_pt[i], 
                event.SDVGenPart_eta[i], 
                event.SDVGenPart_phi[i],
              ))

        print("Event: {} SDVGenVtx: {}".format(ievent, event.nSDVGenVtx))
        for iv in range(event.nSDVGenVtx):
            print('GenVtx  ! {:3d} ! {:7.2f} {:7.2f} {:7.2f} !'.format(
                iv,
                event.SDVGenVtx_x[iv],
                event.SDVGenVtx_y[iv],
                event.SDVGenVtx_z[iv],
            ))
            for ip in range(event.nSDVGenPart):
                if event.SDVGenPart_svxIdx[ip] == iv:
                    print("GenPart ! {:3d} ! {:3d} ! {:8d} {:6d} ! {:9.2f} {:9.2f} {:9.2f} !".format(
                        ip,
                        event.SDVGenPart_genPartIdxMother[ip],
                        event.SDVGenPart_pdgId[ip],
                        event.SDVGenPart_status[ip],
                        event.SDVGenPart_pt[ip], 
                        event.SDVGenPart_eta[ip], 
                        event.SDVGenPart_phi[ip],
                    ))                    
        print("Event: {} nSDVTrack: {}".format(ievent, event.nSDVTrack))
        for it in range(event.nSDVTrack):
            print("Track  ! {:3d} ! {:9.2f} {:9.2f} {:9.2f} {:9.2f} {:9.2f} !".format(
                it,
                event.SDVTrack_pt[it],
                event.SDVTrack_eta[it],
                event.SDVTrack_phi[it],
                event.SDVTrack_dxy[it],
                event.SDVTrack_dz[it]
            ))
         

if __name__ == "__main__":
   main()
