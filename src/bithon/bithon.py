import argparse
import time
import os

def command_gls(args):
  print("bithon::gls starts.")
  start = time.time()
  from bithon.get_longest_seq import gls_main
  gls_main(args)
  print("Time elapsed: {:,} sec.".format(int(time.time() - start)))
  print("bithon::ncbi_gls ends.")


def command_ensgls(args):
  print("bithon::ensembl_gls starts.")
  start = time.time()
  from bithon.ensembl_gls import ensembl_gls
  ensembl_gls(args.infile, args.outfile, args.header)
  print("Time elapsed: {:,} sec.".format(int(time.time() - start)))
  print("bithon::ensembl_gls ends.")


def command_prank(args):
  print("bithon::codon_alignment starts.")
  start = time.time()
  from bithon.codon_alignment import codon_alignment
  params = {
    'nuc': args.infile,
    'out': args.outfile,
    'prank_exe': args.prank_exe
  }
  codon_alignment(params)
  print("Time elapsed: {:,} sec.".format(int(time.time() - start)))
  print("bithon::codon_alignment ends.")


def main():
  parser = argparse.ArgumentParser()
  subparsers = parser.add_subparsers()

  # ncbi_gls
  help_txt = "Extract the longest isoforms from NCBI refseq fasta files."
  help_txt += " See `bithon gls -h`"
  parser_gls = subparsers.add_parser("gls", help = help_txt)
  parser_gls.add_argument("-i", "--indir",
                          help = "PATH to directory that contains `cds_from_genomic.fna` and `protein.faa`.")
  parser_gls.add_argument("-o", "--outdir",
                          help = "PATH to output directory.")
  parser_gls.add_argument("-p", "--prefix", default = "longest",
                          help = """default=%(default)s: Prefix of files.
                          `longest.cds.fa` and `longest.pep.fa` will be generated by default.""")
  parser_gls.add_argument("--keep_identity", action = "store_true",
                          help = "Whether keep only seqs that has no mismatches between Protein and translated CDS.")
  parser_gls.add_argument("--header", choices = ["original", "gene"], default = "original",
                          help = """'original' or 'gene'. Type of fasta header.
                          Original sequence ID will be used by default (`original`).
                          Gene_symbol+species_name will be used when `gene`.""")
  parser_gls.add_argument("--report", default = None,
                          help = "Path to report file (.tsv). Ungenerated by default.")
  parser_gls.set_defaults(handler=command_gls)

  # ensembl_gls
  help_txt = "Extract the longest isoforms from ENSEMBL sequences fasta files."
  help_txt += " See `bithon ensgls -h`"
  parser_egls = subparsers.add_parser("ensgls", help = help_txt)
  parser_egls.add_argument("-i", "--infile")
  parser_egls.add_argument("-o", "--outfile")
  parser_egls.add_argument("--header", choices=["transcript", "id", "symbol"])
  parser_egls.set_defaults(handler=command_ensgls)

  # codon_alignment
  help_txt = "Helper command to use `prank` codon alignment."
  help_txt += " See `bithon prank -h`"
  parser_prank = subparsers.add_parser("prank", help = help_txt)
  parser_prank.add_argument("-i", "--infile")
  parser_prank.add_argument("-o", "--outfile")
  parser_prank.add_argument("--prank_exe", default="prank")
  parser_prank.set_defaults(handler=command_prank)

  args = parser.parse_args()
  if hasattr(args, "handler"):
    args.handler(args)
  else:
    parser.print_help()


if __name__ == "__main__":
  main()
