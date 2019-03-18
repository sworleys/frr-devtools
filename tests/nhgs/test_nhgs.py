import os, sys, subprocess, re, time
from pprint import pprint


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
this_dir = os.path.dirname(os.path.realpath(__file__))
ref_file = '%s/nexthop-group.ref' % (this_dir)


def test_read_nhgs():
    """Testing if the kernel nexthops were read in properly."""

    print("\n\n** Verifying nexthops read from kernel")
    print("*******************************************\n")

    print("Verify show nexthop-group")
    print("-------------------------\n")

    result = str(subprocess.getoutput('vtysh -c "show nexthop-group"'))\
            .expandtabs(8)

    with open(ref_file) as f:
        groups = f.read().strip().rsplit('\n\n')
        for group in groups:
            print(group)
            assert group in result,\
                (
                "\nExpected"
                "\n----------"
                "\n%s"
                "\nActual"
                "\n----------"
                "\n%s"\
                    % (group, result)\
                )

def test_del_nhg():
    """Testing delete nexthop still used re-install."""

    print("\n\n** Verifying nexthop still used re-install")
    print("*******************************************\n")

    with open(ref_file) as f:
        # Delete a nexthop still being referenced
        groups = f.read().strip().rsplit('\n\n')
        g_id = 0
        g_refcnt = 0

        for group in groups:
            g_id = int(re.findall(r'(?:ID: )([0-9]+)', group)[0])
            g_refcnt = int(re.findall(r'(?:RefCnt: )([0-9]+)', group)[0])
            if g_refcnt:
                break

        subprocess.run('ip next del id %d' % g_id, shell=True)
        time.sleep(2)
        result = str(subprocess.getoutput('ip next ls'))
        assert str(g_id) in result
