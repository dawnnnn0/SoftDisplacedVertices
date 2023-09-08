#!/usr/bin/env python

from __future__ import print_function

import click
import ROOT

@click.command()
@click.argument("input", type=click.Path(dir_okay=False, exists=True))
def main(input):
    
    rfile = ROOT.TFile.Open(input, "READ")

    for ievent, event in enumerate(rfile.Events):
        print("Event: {} GenPart: {}".format(ievent, event.nGenPart))
        for i in range(event.nGenPart):
            print("! {:3d} ! {:3d} ! {:8d} {:6d} ! {:9.2f} {:9.2f} {:9.2f} ! {:7.2f} {:7.2f} {:7.2f} !".format(
                i,
                event.GenPart_genPartIdxMother[i],
                event.GenPart_pdgId[i],
                event.GenPart_status[i],
                event.GenPart_pt[i], 
                event.GenPart_eta[i], 
                event.GenPart_phi[i],
                event.GenPart_vx[i], 
                event.GenPart_vy[i], 
                event.GenPart_vz[i],
            ))
        print("Event: {} GenSVX: {}".format(ievent, event.nGenSVX))
        for iv in range(event.nGenSVX):
            print('! {:2d} ! {:7.2f} {:7.2f} {:7.2f} !'.format(
                iv,
                event.GenSVX_x[iv],
                event.GenSVX_y[iv],
                event.GenSVX_z[iv],
            ))
            for ip in range(event.nGenPart):
                if event.GenPart_svxIdx[ip] == iv:
                    print("! {:3d} ! {:3d} ! {:8d} {:6d} ! {:9.2f} {:9.2f} {:9.2f} ! {:7.2f} {:7.2f} {:7.2f} !".format(
                        ip,
                        event.GenPart_genPartIdxMother[ip],
                        event.GenPart_pdgId[ip],
                        event.GenPart_status[ip],
                        event.GenPart_pt[ip], 
                        event.GenPart_eta[ip], 
                        event.GenPart_phi[ip],
                        event.GenPart_vx[ip], 
                        event.GenPart_vy[ip], 
                        event.GenPart_vz[ip],
                    ))                    
        


if __name__ == "__main__":
   main()
