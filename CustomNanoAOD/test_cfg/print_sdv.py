#!/usr/bin/env python

from __future__ import print_function

import click
import ROOT

@click.command()
@click.argument("input", type=click.Path(dir_okay=False, exists=True))
@click.option("--first", default=0)
@click.option("--number", default=-1)
def main(input, first, number):
    
    rfile = ROOT.TFile.Open(input, "READ")

    for ievent, event in enumerate(rfile.Events):
        if first > ievent:
            continue
        if number > 0 and first + number <= ievent:
            break
        print("Event: {} GenPart: {}".format(ievent, event.nGenPart))
        for i in range(event.nSDVGenPart):
            print("! {:3d} ! {:3d} ! {:8d} {:6d} ! {:9.2f} {:9.2f} {:9.2f} ! {:7.2f} {:7.2f} {:7.2f} !".format(
                i,
                event.SDVGenPart_genPartIdxMother[i],
                event.SDVGenPart_pdgId[i],
                event.SDVGenPart_status[i],
                event.SDVGenPart_pt[i], 
                event.SDVGenPart_eta[i], 
                event.SDVGenPart_phi[i],
                event.SDVGenPart_vx[i], 
                event.SDVGenPart_vy[i], 
                event.SDVGenPart_vz[i],
            ))
        print("Event: {} SDVGenVtx: {}".format(ievent, event.nGenSVX))
        for iv in range(event.nGenSVX):
            print('! {:2d} ! {:7.2f} {:7.2f} {:7.2f} !'.format(
                iv,
                event.SDVGenVtx_x[iv],
                event.SDVGenVtx_y[iv],
                event.SDVGenVtx_z[iv],
            ))
            for ip in range(event.nGenPart):
                if event.GenPart_svxIdx[ip] == iv:
                    print("! {:3d} ! {:3d} ! {:8d} {:6d} ! {:9.2f} {:9.2f} {:9.2f} !".format(
                        ip,
                        event.SDVGenPart_genPartIdxMother[ip],
                        event.SDVGenPart_pdgId[ip],
                        event.SDVGenPart_status[ip],
                        event.SDVGenPart_pt[ip], 
                        event.SDVGenPart_eta[ip], 
                        event.SDVGenPart_phi[ip],
                    ))                    
        


if __name__ == "__main__":
   main()
